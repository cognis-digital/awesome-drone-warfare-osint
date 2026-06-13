#!/usr/bin/env python3
"""
scripts/headline_numbers.py
===========================

Replaces the HEADLINE-NUMBERS block in README.md with fresh counts
computed from data/*.csv. Idempotent. Use in a CI step:

    python scripts/headline_numbers.py
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
README = ROOT / "README.md"

START = "<!-- HEADLINE-NUMBERS-START -->"
END = "<!-- HEADLINE-NUMBERS-END -->"


def render(table: dict[str, str]) -> str:
    lines = [
        START,
        "| | Count | Primary source |",
        "|---|---|---|",
    ]
    for k, (v, src) in table.items():
        lines.append(f"| {k} | **{v}** | {src} |")
    lines.append(END)
    return "\n".join(lines)


def main() -> int:
    components = pd.read_csv(DATA / "components.csv")
    drones = pd.read_csv(DATA / "drones.csv")
    manufacturers = pd.read_csv(DATA / "manufacturers.csv")
    incidents = pd.read_csv(DATA / "incidents.csv") if (DATA / "incidents.csv").exists() else pd.DataFrame()
    countries = sorted(set(components["manufacturer_country"]) - {"UNK", ""})

    today = date.today().isoformat()
    table = {
        "Drone platforms documented": (
            f"{len(drones):,}",
            "GUR + CAR + IISS aggregation"
        ),
        "Foreign components catalogued": (
            f"{len(components):,}",
            "[GUR War & Sanctions](https://war-sanctions.gur.gov.ua/en/components) + NACP"
        ),
        "Manufacturers identified": (
            f"{len(manufacturers):,}",
            "cross-linked to OpenSanctions"
        ),
        "Countries of origin": (
            f"{len(countries):,}",
            "weighted by component count"
        ),
        "Strike incidents geo-tagged": (
            f"{len(incidents):,}" if len(incidents) else "—",
            "ACLED + OSINT timeline (join-only, not redistributed)"
        ),
        "Last sync": (
            today, "weekly GitHub Action cron"
        ),
    }

    txt = README.read_text(encoding="utf-8")
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    new = pat.sub(render(table), txt)
    README.write_text(new, encoding="utf-8")
    print("README headline numbers updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
