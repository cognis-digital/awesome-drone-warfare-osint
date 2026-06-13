#!/usr/bin/env python3
"""
car_field_dispatches.py
=======================

Index of Conflict Armament Research field dispatches. CAR publishes
forensic reports as long-form HTML and PDFs. We don't redistribute
their content; we index the page so each `data/teardowns.csv` row has
an authoritative URL.

USAGE
-----
    python scrapers/car_field_dispatches.py --out-dir data/
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.conflictarm.com"
INDEX = f"{BASE}/field-dispatches/"
USER_AGENT = (
    "awesome-drone-warfare-osint/0.1 (+https://github.com/USER/"
    "awesome-drone-warfare-osint; research/sanctions-enforcement)"
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default="data")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    sess = requests.Session()
    sess.headers["User-Agent"] = USER_AGENT
    logging.info("GET %s", INDEX)
    r = sess.get(INDEX, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    teardowns = []
    for a in soup.select("a"):
        href = a.get("href", "")
        text = a.get_text(" ", strip=True)
        if not href or len(text) < 8:
            continue
        if "field-dispatch" in href or "/perspectives/" in href:
            url = urljoin(BASE, href)
            teardowns.append({
                "teardown_id": f"car-{abs(hash(url)) % 10_000_000}",
                "title": text[:480],
                "drone_id": "",
                "organization": "Conflict Armament Research",
                "url": url,
                "published_date": date.today().isoformat(),
                "doi": "",
                "is_pdf": str(url.lower().endswith(".pdf")).lower(),
                "components_referenced": 0,
                "notes": "Indexed from CAR Field Dispatches page",
            })
    time.sleep(1.0)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if teardowns:
        with (out / "teardowns_car.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(teardowns[0].keys()))
            w.writeheader()
            w.writerows(teardowns)
        logging.info("Wrote %d teardown rows", len(teardowns))
    else:
        logging.warning("No teardowns found on %s", INDEX)
    return 0


if __name__ == "__main__":
    sys.exit(main())
