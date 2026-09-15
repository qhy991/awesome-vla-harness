#!/usr/bin/env python3
"""Check that every URL in data/projects.yaml and the Markdown files resolves.

Uses only the standard library. HEAD first, falling back to GET for hosts that
reject HEAD (arxiv.org among them).

Usage:
    python scripts/check_links.py
    python scripts/check_links.py --changed-only      # only URLs in `git diff`
    python scripts/check_links.py --timeout 20 --workers 8
"""

from __future__ import annotations

import argparse
import concurrent.futures
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
USER_AGENT = "awesome-vla-harness-link-checker/1.0 (+https://github.com/)"

URL_RE = re.compile(r"https?://[^\s<>\"'\)\]`,]+")

# Placeholders that intentionally do not resolve.
SKIP_SUBSTRINGS = (
    "github.com/OWNER/",
    "example.com",
    "localhost",
    "127.0.0.1",
)

# Form-placeholder fragments such as `https://github.com/...` in issue templates.
SKIP_EXACT = {
    "https://github.com",
    "https://github.com/",
}

SCAN_SUFFIXES = {".md", ".yaml", ".yml", ".cff", ".json"}
SCAN_DIRS = ("", "data", "docs", "entries", "examples", "docker", ".github")


def iter_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        rel = path.relative_to(ROOT)
        if any(part in {".git", ".venv", "node_modules", "__pycache__"} for part in rel.parts):
            continue
        files.append(path)
    return sorted(files)


def collect_urls(changed_only: bool) -> dict[str, set[str]]:
    """Return {url: {source files}}."""
    urls: dict[str, set[str]] = {}

    if changed_only:
        try:
            diff = subprocess.run(
                ["git", "diff", "HEAD", "--unified=0"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            ).stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("warn: could not run git diff; falling back to a full scan")
            return collect_urls(changed_only=False)
        for line in diff.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                for url in URL_RE.findall(line):
                    urls.setdefault(url.rstrip(".,;:"), set()).add("<git diff>")
        return urls

    for path in iter_files():
        rel = str(path.relative_to(ROOT))
        for url in URL_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
            urls.setdefault(url.rstrip(".,;:"), set()).add(rel)
    return urls


def should_skip(url: str) -> bool:
    return url in SKIP_EXACT or any(token in url for token in SKIP_SUBSTRINGS)


def probe(url: str, timeout: float, retries: int = 2) -> tuple[str, int | None, str]:
    """Return (url, status_code_or_None, message), retrying transient failures."""
    result = _probe_once(url, timeout)
    attempt = 1
    # Only network-level failures (status is None) are worth retrying; an HTTP
    # status is a real answer from the server.
    while result[1] is None and attempt <= retries:
        time.sleep(1.5 * attempt)
        result = _probe_once(url, timeout)
        attempt += 1
    return result


def _probe_once(url: str, timeout: float) -> tuple[str, int | None, str]:
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return url, response.status, "ok"
        except urllib.error.HTTPError as exc:
            # Some hosts reject HEAD with 403/405; retry once with GET.
            if method == "HEAD" and exc.code in (403, 405, 400, 501):
                continue
            return url, exc.code, f"HTTP {exc.code}"
        except urllib.error.URLError as exc:
            if method == "HEAD":
                continue
            return url, None, f"{type(exc).__name__}: {exc.reason}"
        except Exception as exc:  # noqa: BLE001 - report, never crash the run
            if method == "HEAD":
                continue
            return url, None, f"{type(exc).__name__}: {exc}"
    return url, None, "unreachable"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--retries", type=int, default=2, help="retries for network-level failures")
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument(
        "--allow-forbidden",
        action="store_true",
        default=True,
        help="treat 403/429 as pass (bot protection, not a broken link)",
    )
    args = parser.parse_args()

    urls = collect_urls(args.changed_only)
    checked = {u: s for u, s in urls.items() if not should_skip(u)}
    skipped = len(urls) - len(checked)

    if not checked:
        print("no URLs to check")
        return 0

    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(probe, url, args.timeout, args.retries): url for url in sorted(checked)}
        for future in concurrent.futures.as_completed(futures):
            url, status, message = future.result()
            ok = status is not None and (
                status < 400 or (args.allow_forbidden and status in (403, 429))
            )
            print(f"{'PASS' if ok else 'FAIL'} {status or '---':>4}  {url}")
            if not ok:
                sources = ", ".join(sorted(checked[url]))
                failures.append(f"{url}  ({message})  ← {sources}")

    print(f"\nchecked {len(checked)} urls, skipped {skipped} placeholder(s)")
    if failures:
        print("\nbroken links:")
        for failure in failures:
            print(f"  {failure}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
