#!/usr/bin/env python3
"""Render the two activity charts from data/projects.yaml.

    assets/stars-by-project.svg        horizontal bars on a log10(stars + 1) scale
    assets/maintenance-freshness.svg   days since last push, bucketed

Two charts on purpose: popularity and maintenance freshness must not be
collapsed into a single number. The log scale exists so that a 27k-star stack
does not visually erase a 600-star harness.

Reads only the automation-owned `github_snapshot` blocks, so run
`scripts/update_github_stats.py` first. Standard library only.

Usage:
    python scripts/render_charts.py [--out-dir assets]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import math
import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("error: PyYAML is required. Run: python -m pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "data" / "projects.yaml"

BUCKETS = [
    ("0–30 days", 0, 30),
    ("31–90 days", 31, 90),
    ("91–365 days", 91, 365),
    (">365 days", 366, 10**6),
]
INACTIVE_MATURITY = {"maintenance", "archived"}

STYLE = """
  <style>
    .bg { fill: #ffffff; }
    .label, .value, .title, .sub { font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; }
    .title { font-size: 15px; font-weight: 600; fill: #111827; }
    .sub   { font-size: 11px; fill: #6b7280; }
    .label { font-size: 12px; fill: #374151; }
    .value { font-size: 11px; fill: #6b7280; }
    .bar   { fill: #2563eb; }
    .bar-alt { fill: #7c3aed; }
    .axis  { stroke: #e5e7eb; stroke-width: 1; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #0b0f19; }
      .title { fill: #f3f4f6; }
      .sub, .value { fill: #9ca3af; }
      .label { fill: #d1d5db; }
      .bar { fill: #60a5fa; }
      .bar-alt { fill: #a78bfa; }
      .axis { stroke: #1f2937; }
    }
  </style>
"""


def load() -> list[dict]:
    return yaml.safe_load(PROJECTS.read_text(encoding="utf-8"))


def days_since(timestamp: str, today: dt.date) -> int | None:
    try:
        parsed = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date()
    except (ValueError, AttributeError):
        return None
    return (today - parsed).days


def svg_open(width: int, height: int, title: str, subtitle: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{html.escape(title)}">',
        STYLE,
        f'<rect class="bg" width="{width}" height="{height}" rx="8"/>',
        f'<text class="title" x="20" y="28">{html.escape(title)}</text>',
        f'<text class="sub" x="20" y="46">{html.escape(subtitle)}</text>',
    ]


def render_stars(entries: list[dict], fetched_at: str) -> str:
    rows = [
        (entry["name"], entry["github_snapshot"]["stars"])
        for entry in entries
        if (entry.get("github_snapshot") or {}).get("stars") is not None
    ]
    rows.sort(key=lambda row: row[1], reverse=True)

    left, row_h, top = 210, 26, 70
    width, height = 760, top + max(len(rows), 1) * row_h + 30
    bar_max = width - left - 90
    scale_max = max((math.log10(value + 1) for _, value in rows), default=1.0) or 1.0

    out = svg_open(
        width,
        height,
        "Stars by project (log scale)",
        f"log10(stars + 1) · popularity only, not maturity · fetched {fetched_at}",
    )
    out.append(f'<line class="axis" x1="{left}" y1="{top - 10}" x2="{left}" y2="{height - 20}"/>')

    for index, (name, stars) in enumerate(rows):
        y = top + index * row_h
        bar_w = max(2, int(bar_max * math.log10(stars + 1) / scale_max))
        out.append(f'<text class="label" x="{left - 10}" y="{y + 13}" text-anchor="end">{html.escape(name)}</text>')
        out.append(f'<rect class="bar" x="{left}" y="{y + 3}" width="{bar_w}" height="14" rx="3"/>')
        out.append(f'<text class="value" x="{left + bar_w + 8}" y="{y + 14}">{stars:,}</text>')

    if not rows:
        out.append('<text class="value" x="20" y="80">no github_snapshot data yet — run update_github_stats.py</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"


def render_freshness(entries: list[dict], fetched_at: str, today: dt.date) -> str:
    counts = {label: 0 for label, _, _ in BUCKETS}
    counts["maintenance / archived"] = 0
    unknown = 0

    for entry in entries:
        if entry.get("maturity") in INACTIVE_MATURITY or (entry.get("github_snapshot") or {}).get("archived"):
            counts["maintenance / archived"] += 1
            continue
        snapshot = entry.get("github_snapshot") or {}
        age = days_since(snapshot.get("last_push", ""), today)
        if age is None:
            unknown += 1
            continue
        for label, low, high in BUCKETS:
            if low <= age <= high:
                counts[label] += 1
                break

    rows = list(counts.items())
    left, row_h, top = 210, 30, 70
    width, height = 760, top + len(rows) * row_h + 40
    bar_max = width - left - 90
    peak = max([count for _, count in rows] + [1])

    out = svg_open(
        width,
        height,
        "Maintenance freshness (days since last push)",
        f"maintenance / archived counted separately · fetched {fetched_at}",
    )
    out.append(f'<line class="axis" x1="{left}" y1="{top - 10}" x2="{left}" y2="{height - 30}"/>')

    for index, (label, count) in enumerate(rows):
        y = top + index * row_h
        bar_w = max(2, int(bar_max * count / peak)) if count else 2
        out.append(f'<text class="label" x="{left - 10}" y="{y + 15}" text-anchor="end">{html.escape(label)}</text>')
        out.append(f'<rect class="bar-alt" x="{left}" y="{y + 4}" width="{bar_w}" height="16" rx="3"/>')
        out.append(f'<text class="value" x="{left + bar_w + 8}" y="{y + 17}">{count}</text>')

    if unknown:
        out.append(f'<text class="value" x="{left}" y="{height - 12}">{unknown} project(s) without snapshot data</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=pathlib.Path, default=ROOT / "assets")
    args = parser.parse_args()

    entries = load()
    today = dt.date.today()
    fetched = next(
        (
            (entry.get("github_snapshot") or {}).get("fetched_at")
            for entry in entries
            if (entry.get("github_snapshot") or {}).get("fetched_at")
        ),
        "n/a",
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "stars-by-project.svg").write_text(render_stars(entries, fetched), encoding="utf-8")
    (args.out_dir / "maintenance-freshness.svg").write_text(
        render_freshness(entries, fetched, today), encoding="utf-8"
    )
    print(f"wrote {args.out_dir / 'stars-by-project.svg'}")
    print(f"wrote {args.out_dir / 'maintenance-freshness.svg'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
