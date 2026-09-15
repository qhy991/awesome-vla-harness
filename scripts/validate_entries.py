#!/usr/bin/env python3
"""Validate data/projects.yaml against data/schema.json and cross-check entries/*.md.

Uses `jsonschema` when available; otherwise falls back to a built-in structural
check covering the same required fields and enums.

Usage:
    python scripts/validate_entries.py [--stale-days 180]

Exit code 0 on success, 1 on any error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("error: PyYAML is required. Run: python -m pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "data" / "projects.yaml"
SCHEMA = ROOT / "data" / "schema.json"
ENTRIES_DIR = ROOT / "entries"

REQUIRED = [
    "id",
    "name",
    "organization",
    "url",
    "category",
    "license",
    "capabilities",
    "backends",
    "deployment",
    "evaluation",
    "maturity",
    "last_verified",
    "references",
]

REQUIRED_CAPABILITIES = [
    "model_adapter",
    "benchmark_adapter",
    "scheduler",
    "parallel_rollout",
    "sandbox",
    "observability",
    "plugin_system",
]

CATEGORIES = {
    "vla-evaluation",
    "llm-evaluation",
    "agent-runtime",
    "robotics-stack",
    "benchmark",
    "simulator",
    "model-serving",
    "observability",
    "deployment",
    "safety-evaluation",
    "harness-evolution",
    "research",
}

MATURITY = {"emerging", "active", "mature", "stable", "maintenance", "archived"}

# Fields that automation owns and contributors must not hand-edit.
AUTOMATED_FIELDS = {"github_snapshot"}

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _normalize(value):
    """YAML parses bare `2026-09-14` into a date object; the schema expects a string."""
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    return value


def load() -> list[dict]:
    with PROJECTS.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, list):
        raise SystemExit("error: data/projects.yaml must contain a top-level list")
    return _normalize(data)


def schema_validate(data: list[dict], errors: list[str]) -> bool:
    """Validate with jsonschema if installed. Returns True if it actually ran."""
    try:
        import jsonschema
    except ImportError:
        return False
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"schema: {path}: {err.message}")
    return True


def structural_check(data: list[dict], errors: list[str]) -> None:
    """Fallback checks, also run alongside jsonschema for repo-specific rules."""
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()

    for index, entry in enumerate(data):
        where = f"entry[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{where}: must be a mapping")
            continue

        pid = entry.get("id", f"<missing id at {index}>")
        where = f"{pid}"

        for field in REQUIRED:
            if field not in entry or entry[field] in (None, "", [], {}):
                errors.append(f"{where}: missing required field '{field}'")

        if isinstance(pid, str) and not ID_RE.match(pid):
            errors.append(f"{where}: id must be kebab-case [a-z0-9-]")
        if pid in seen_ids:
            errors.append(f"{where}: duplicate id")
        seen_ids.add(pid)

        url = entry.get("url")
        if isinstance(url, str):
            if not url.startswith(("http://", "https://")):
                errors.append(f"{where}: url must be an http(s) URL")
            if url in seen_urls:
                errors.append(f"{where}: duplicate url {url}")
            seen_urls.add(url)

        for field in ("category", "backends", "deployment", "evaluation", "references"):
            value = entry.get(field)
            if value is not None and not isinstance(value, list):
                errors.append(f"{where}: '{field}' must be a list")

        for cat in entry.get("category") or []:
            if cat not in CATEGORIES:
                errors.append(f"{where}: unknown category '{cat}'")

        if entry.get("maturity") not in MATURITY and "maturity" in entry:
            errors.append(f"{where}: unknown maturity '{entry.get('maturity')}'")

        lic = entry.get("license")
        if isinstance(lic, dict):
            if not lic.get("code"):
                errors.append(f"{where}: license.code is required")
        elif "license" in entry:
            errors.append(f"{where}: license must be a mapping with a 'code' key")

        caps = entry.get("capabilities")
        if isinstance(caps, dict):
            for cap in REQUIRED_CAPABILITIES:
                if cap not in caps:
                    errors.append(f"{where}: capabilities.{cap} is required")
            for cap, value in caps.items():
                if cap == "plugin_system":
                    if not isinstance(value, str):
                        errors.append(f"{where}: capabilities.plugin_system must be a string")
                elif not (isinstance(value, bool) or value == "partial"):
                    errors.append(
                        f"{where}: capabilities.{cap} must be true/false/'partial'"
                    )
        elif "capabilities" in entry:
            errors.append(f"{where}: capabilities must be a mapping")

        lv = entry.get("last_verified")
        if isinstance(lv, dt.date):
            lv = lv.isoformat()
        if isinstance(lv, str) and not DATE_RE.match(lv):
            errors.append(f"{where}: last_verified must be YYYY-MM-DD")

        for ref in entry.get("references") or []:
            if not isinstance(ref, str) or not ref.startswith(("http://", "https://")):
                errors.append(f"{where}: reference '{ref}' must be an http(s) URL")

        snap = entry.get("github_snapshot")
        if snap is not None:
            if not isinstance(snap, dict) or "fetched_at" not in snap:
                errors.append(
                    f"{where}: github_snapshot must be a mapping containing 'fetched_at'"
                )


def check_markdown_coverage(data: list[dict], errors: list[str]) -> None:
    """Every project url should appear in at least one entries/*.md file."""
    corpus = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(ENTRIES_DIR.glob("*.md"))
    )
    for entry in data:
        url = entry.get("url")
        if isinstance(url, str) and url not in corpus:
            errors.append(
                f"{entry.get('id')}: url not referenced by any entries/*.md "
                f"(add a short description there)"
            )


def check_staleness(data: list[dict], stale_days: int, warnings: list[str]) -> None:
    today = dt.date.today()
    for entry in data:
        lv = entry.get("last_verified")
        if isinstance(lv, str):
            try:
                lv = dt.date.fromisoformat(lv)
            except ValueError:
                continue
        if isinstance(lv, dt.date):
            age = (today - lv).days
            if age > stale_days:
                warnings.append(
                    f"{entry.get('id')}: last_verified is {age} days old "
                    f"(>{stale_days}); please re-verify"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stale-days",
        type=int,
        default=180,
        help="warn when last_verified is older than this many days (default: 180)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat staleness warnings as errors",
    )
    args = parser.parse_args()

    data = load()
    errors: list[str] = []
    warnings: list[str] = []

    ran_schema = schema_validate(data, errors)
    structural_check(data, errors)
    check_markdown_coverage(data, errors)
    check_staleness(data, args.stale_days, warnings)

    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"ERROR {error}")

    mode = "jsonschema + structural" if ran_schema else "structural only (jsonschema not installed)"
    print(f"\nchecked {len(data)} entries [{mode}]")

    if errors or (args.strict and warnings):
        print("FAILED")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
