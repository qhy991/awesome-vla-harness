#!/usr/bin/env python3
"""Refresh the automation-owned `github_snapshot` block in data/projects.yaml.

Volatile metrics (stars, forks, last push, open items) must never be hand-written
into the Markdown. They live here, always carrying a `fetched_at` timestamp.

Note: GitHub's `open_issues_count` includes BOTH issues and pull requests, which
is why this script writes it as `open_items`.

Usage:
    GITHUB_TOKEN=... python scripts/update_github_stats.py
    python scripts/update_github_stats.py --dry-run
    python scripts/update_github_stats.py --json-out assets/stats.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("error: PyYAML is required. Run: python -m pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "data" / "projects.yaml"

GITHUB_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+)")
API = "https://api.github.com/repos/{owner}/{repo}"


def repo_slug(url: str) -> tuple[str, str] | None:
    match = GITHUB_RE.match(url or "")
    if not match:
        return None
    owner, repo = match.group(1), match.group(2)
    # Never try to fetch stats for placeholders or for this repository itself.
    if owner == "OWNER" or (owner, repo.removesuffix(".git")) == ("qhy991", "awesome-vla-harness"):
        return None
    return owner, repo.removesuffix(".git")


def fetch(owner: str, repo: str, token: str | None, timeout: float) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-vla-harness-stats/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(API.format(owner=owner, repo=repo), headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def snapshot(payload: dict, fetched_at: str) -> dict:
    return {
        "fetched_at": fetched_at,
        "stars": payload.get("stargazers_count"),
        "forks": payload.get("forks_count"),
        "last_push": payload.get("pushed_at"),
        # GitHub's open_issues_count includes pull requests.
        "open_items": payload.get("open_issues_count"),
        "archived": bool(payload.get("archived", False)),
    }


def replace_block(text: str, entry_id: str, block: dict) -> str:
    """Rewrite (or append) the github_snapshot block for one entry, in place.

    Operates on raw text so that comments and formatting elsewhere survive.
    """
    lines = text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines):
        if line.rstrip("\n") == f"- id: {entry_id}":
            start = index
            break
    if start is None:
        return text

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("- id: "):
            end = index
            break

    rendered = ["\n", "  github_snapshot:\n"]
    for key, value in block.items():
        if value is None:
            continue
        if isinstance(value, bool):
            rendered.append(f"    {key}: {'true' if value else 'false'}\n")
        elif isinstance(value, int):
            rendered.append(f"    {key}: {value}\n")
        else:
            rendered.append(f'    {key}: "{value}"\n')

    body = lines[start:end]
    snap_start = None
    for index, line in enumerate(body):
        if line.rstrip("\n") == "  github_snapshot:":
            snap_start = index
            break

    if snap_start is None:
        while body and body[-1].strip() == "":
            body.pop()
        body.extend(rendered)
        body.append("\n")
    else:
        snap_end = snap_start + 1
        while snap_end < len(body) and (
            body[snap_end].startswith("    ") or body[snap_end].strip() == ""
        ):
            if body[snap_end].strip() == "" and snap_end + 1 < len(body) and not body[
                snap_end + 1
            ].startswith("    "):
                break
            snap_end += 1
        body[snap_start:snap_end] = rendered[1:]

    return "".join(lines[:start] + body + lines[end:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--json-out", type=pathlib.Path, default=None)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("warn: no GITHUB_TOKEN set; unauthenticated rate limit is 60 req/hour")

    fetched_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = PROJECTS.read_text(encoding="utf-8")
    data = yaml.safe_load(text)

    collected: list[dict] = []
    updated = 0

    for entry in data:
        entry_id = entry["id"]
        slug = repo_slug(entry.get("url", ""))
        if slug is None:
            print(f"skip  {entry_id} (not a GitHub repo url)")
            continue
        owner, repo = slug
        try:
            payload = fetch(owner, repo, token, args.timeout)
        except urllib.error.HTTPError as exc:
            print(f"FAIL  {entry_id}: HTTP {exc.code}")
            continue
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL  {entry_id}: {type(exc).__name__}: {exc}")
            continue

        block = snapshot(payload, fetched_at)
        collected.append({"project": entry_id, "stats": block})
        print(
            f"ok    {entry_id:<28} stars={block['stars']:<7} forks={block['forks']:<6} "
            f"last_push={block['last_push']}"
        )
        text = replace_block(text, entry_id, block)
        updated += 1

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps({"fetched_at": fetched_at, "projects": collected}, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.json_out}")

    if args.dry_run:
        print(f"\ndry-run: would update {updated} entries")
        return 0

    PROJECTS.write_text(text, encoding="utf-8")
    print(f"\nupdated {updated} entries in {PROJECTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
