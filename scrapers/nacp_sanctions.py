#!/usr/bin/env python3
"""
nacp_sanctions.py
=================

Polite, schema-friendly scraper for Ukraine's NACP "War & Sanctions"
sister portal (Trap.org.ua) Tools-of-War module.

NOTE: this file is a thin stub that mirrors the structure of
`gur_war_sanctions.py`. NACP exposes a similar HTML structure and
several JSON endpoints; the heavy lifting follows the same pattern.
Implement the page parser when you stand up the repo against the
live portal.

USAGE
-----
    python scrapers/nacp_sanctions.py --out-dir data/
"""
from __future__ import annotations

import argparse
import logging
import sys

BASE = "https://trap.org.ua"
INDEX = f"{BASE}/en/publications/"

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default="data")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.info("NACP scraper stub. Implement against %s", INDEX)
    logging.info("Output directory: %s", args.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
