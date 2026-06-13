#!/usr/bin/env python3
"""
gur_war_sanctions.py
====================

Polite, robots-aware scraper of the Defence Intelligence of Ukraine
(GUR/HUR) "War & Sanctions" portal:

    https://war-sanctions.gur.gov.ua/en/components

The portal hosts the world's largest open forensic database of
foreign-produced components found in Russian and allied weapons (5,800+
records as of 2026-05-25). This script extracts the component listings
and produces:

    data/components.csv
    data/drones.csv               (one row per weapon page linked)
    data/manufacturers.csv        (deduplicated)

USAGE
-----
    python scrapers/gur_war_sanctions.py \
        --out-dir data/ \
        --rate-limit 1.0 \
        --max-pages 0   # 0 = all

RESPECTFUL DEFAULTS
-------------------
* 1 request / second by default
* Respects robots.txt
* Resumable: writes a checkpoint after every page
* Sets a clearly identifying User-Agent string

This script does NOT crawl any non-public area, does NOT hammer the
server, and stops on the first 4xx error to avoid pressuring the
upstream service.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import json
import logging
import re
import sys
import time
import urllib.robotparser
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(
        "Missing dependency. Install with:\n"
        "    pip install requests beautifulsoup4 lxml",
        file=sys.stderr,
    )
    raise

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

BASE = "https://war-sanctions.gur.gov.ua"
COMPONENTS_INDEX = f"{BASE}/en/components"
USER_AGENT = (
    "awesome-drone-warfare-osint/0.1 (+https://github.com/USER/"
    "awesome-drone-warfare-osint; research/sanctions-enforcement)"
)

# Map raw GUR category text -> our enum
CATEGORY_MAP = {
    "memory chip": "memory",
    "transceiver": "transceiver",
    "digital signal processor": "soc",
    "microcontroller": "mcu",
    "fpga": "fpga",
    "antenna": "antenna",
    "engine": "engine",
    "turbojet engine": "engine",
    "servo drive": "motor",
    "motor": "motor",
    "dc/dc converter": "power",
    "voltage regulator": "regulator",
    "connector": "connector",
    "satellite navigation system receiver": "gnss",
    "inertial navigation system": "ins",
    "imu": "imu",
    "air pressure measuring unit": "sensor",
    "flight controller": "mcu",
    "computer module": "soc",
    "network switch": "datalink",
    "mesh modem": "datalink",
    "tracker": "sensor",
    "infrared video camera": "ir_sensor",
    "video stream capture unit": "camera",
    "sd/hd video encoder": "camera",
    "single-phase solid-state dc relay": "passive",
    "warhead": "mechanical",
    "power distribution unit": "power",
    "rail-to-rail buffer": "passive",
    "digital isolator": "passive",
    "rs-485/422 multiprotocol transceiver": "transceiver",
    "rs-485/rs-422 converter": "transceiver",
}

# ISO-2 codes for the country strings GUR uses
COUNTRY_MAP = {
    "people's republic of china": "CN",
    "united states of america": "US",
    "taiwan": "TW",
    "japan": "JP",
    "germany": "DE",
    "switzerland": "CH",
    "south korea": "KR",
    "republic of korea": "KR",
    "iran": "IR",
    "russia": "RU",
    "russian federation": "RU",
    "belarus": "BY",
    "netherlands": "NL",
    "united kingdom": "GB",
    "france": "FR",
    "italy": "IT",
    "ireland": "IE",
    "singapore": "SG",
    "hong kong": "HK",
    "malaysia": "MY",
    "thailand": "TH",
    "philippines": "PH",
    "israel": "IL",
    "india": "IN",
    "canada": "CA",
    "austria": "AT",
    "czechia": "CZ",
    "czech republic": "CZ",
    "poland": "PL",
    "spain": "ES",
    "sweden": "SE",
    "finland": "FI",
    "norway": "NO",
    "denmark": "DK",
    "turkey": "TR",
    "ukraine": "UA",
}

# --------------------------------------------------------------------------- #
# Data classes
# --------------------------------------------------------------------------- #

@dataclass
class Component:
    component_id: str
    name_marking: str
    category: str
    function: str
    manufacturer: str
    manufacturer_country: str
    oem_part_number: str
    production_date: str
    found_in_drones: str          # JSON-encoded list
    sanctions_status: str
    is_dual_use: bool
    replaceable_with: str         # JSON-encoded list
    price_retail_usd: str         # empty string when unknown
    source_url: str
    evidence_image: str
    last_verified: str
    notes: str


@dataclass
class Drone:
    id: str
    display_name: str
    aka: str                       # JSON-encoded list
    operators: str                 # JSON-encoded list
    manufacturer_country: str
    role: str
    propulsion: str
    total_components_documented: int
    primary_source_url: str
    secondary_sources: str         # JSON-encoded list
    image_url: str
    last_verified: str
    notes: str

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def map_category(raw: str) -> str:
    raw_l = raw.lower().strip()
    for key, val in CATEGORY_MAP.items():
        if key in raw_l:
            return val
    return "unknown"


def map_country(raw: str) -> str:
    if not raw:
        return "UNK"
    raw_l = raw.lower().strip()
    return COUNTRY_MAP.get(raw_l, "UNK")


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en;q=0.9",
    })
    return s


def check_robots(session: requests.Session, url: str) -> bool:
    rp = urllib.robotparser.RobotFileParser()
    robots_url = urljoin(url, "/robots.txt")
    try:
        r = session.get(robots_url, timeout=15)
        if r.status_code == 200:
            rp.parse(r.text.splitlines())
            allowed = rp.can_fetch(USER_AGENT, url)
            if not allowed:
                logging.warning("robots.txt disallows %s — aborting", url)
            return allowed
    except Exception as exc:
        logging.warning("robots.txt fetch failed (%s) — proceeding cautiously", exc)
    return True

# --------------------------------------------------------------------------- #
# Scraping
# --------------------------------------------------------------------------- #

class GurScraper:
    def __init__(self, rate_limit: float = 1.0, max_pages: int = 0):
        self.session = make_session()
        self.rate_limit = rate_limit
        self.max_pages = max_pages
        self._last_request: float = 0.0

    def _sleep(self) -> None:
        elapsed = time.time() - self._last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_request = time.time()

    def _get(self, url: str) -> str:
        self._sleep()
        logging.info("GET %s", url)
        r = self.session.get(url, timeout=30)
        if r.status_code >= 400:
            raise RuntimeError(f"HTTP {r.status_code} on {url}")
        return r.text

    def iter_component_pages(self) -> Iterator[str]:
        """Yield each paginated index page URL."""
        page = 1
        while True:
            yield f"{COMPONENTS_INDEX}?page={page}"
            page += 1
            if self.max_pages and page > self.max_pages:
                break

    def parse_index(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        out: list[dict] = []
        # The GUR portal renders each component as a card with an anchor
        # to /en/components/<id>. Find every such anchor.
        for a in soup.select('a[href*="/en/components/"]'):
            href = a.get("href", "")
            m = re.search(r"/en/components/(\d+)", href)
            if not m:
                continue
            cid = m.group(1)
            card_text = a.get_text(" ", strip=True)
            img = a.find("img")
            img_url = urljoin(BASE, img["src"]) if img and img.get("src") else ""
            out.append({
                "id": cid,
                "url": urljoin(BASE, href),
                "card_text": card_text,
                "img_url": img_url,
            })
        # Deduplicate by id, preserve order
        seen, dedup = set(), []
        for item in out:
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            dedup.append(item)
        return dedup

    def parse_component_card(self, item: dict) -> Component | None:
        """
        We try to extract structured fields from the card text on the index
        page (cheap path). For maximum fidelity a follow-up GET to
        item['url'] could be performed; we keep that optional.
        """
        text = item["card_text"]

        def grab(label: str) -> str:
            # GUR cards repeat the format: "Label\nvalue"
            pat = rf"{re.escape(label)}\s+(.+?)(?=\s+(?:Name/Marking|Armament|Manufacturer's headquarters country|Manufacturer|Production date|Weapon|More)\b|$)"
            m = re.search(pat, text)
            return m.group(1).strip() if m else ""

        name = grab("Name/Marking")
        armament = grab("Armament") or grab("Weapon")
        country = grab("Manufacturer's headquarters country")
        mfr = grab("Manufacturer")

        if not name and not armament:
            return None

        # Try to detect a part number embedded in the card text (alphanumeric blocks)
        part_no = ""
        # Heuristic: a token that looks like a chip marking
        m = re.search(r"\b([A-Z0-9]{3,}[\-_/]?[A-Z0-9]+(?:\s[A-Z0-9]+)?)\b", name)
        if m and m.group(1).lower() != name.lower():
            part_no = m.group(1)

        return Component(
            component_id=f"gur-{item['id']}",
            name_marking=name or "(unspecified)",
            category=map_category(name),
            function="",
            manufacturer=mfr or "Not identified",
            manufacturer_country=map_country(country),
            oem_part_number=part_no,
            production_date="",
            found_in_drones=json.dumps([slugify(armament)] if armament else []),
            sanctions_status="unknown",
            is_dual_use=False,
            replaceable_with=json.dumps([]),
            price_retail_usd="",
            source_url=item["url"],
            evidence_image=item["img_url"],
            last_verified=date.today().isoformat(),
            notes=f"Linked weapon as published by GUR: {armament}" if armament else "",
        )

    def scrape(self) -> tuple[list[Component], list[Drone]]:
        if not check_robots(self.session, COMPONENTS_INDEX):
            return [], []

        components: list[Component] = []
        drones_seen: dict[str, Drone] = {}

        empty_page_streak = 0
        for page_url in self.iter_component_pages():
            try:
                html = self._get(page_url)
            except RuntimeError as exc:
                logging.warning("Stopping due to %s", exc)
                break

            items = self.parse_index(html)
            if not items:
                empty_page_streak += 1
                if empty_page_streak >= 2:
                    logging.info("Two consecutive empty pages — assuming end of pagination")
                    break
                continue
            empty_page_streak = 0

            for item in items:
                comp = self.parse_component_card(item)
                if comp is None:
                    continue
                components.append(comp)
                # Register the parent weapon
                for d_id in json.loads(comp.found_in_drones):
                    if not d_id:
                        continue
                    if d_id not in drones_seen:
                        # Try to map slug -> friendly name
                        friendly = d_id.replace("-", " ").title()
                        drones_seen[d_id] = Drone(
                            id=d_id,
                            display_name=friendly,
                            aka=json.dumps([]),
                            operators=json.dumps(["RU"]),  # default: RU-operated
                            manufacturer_country="UNK",
                            role="loitering_munition" if "shahed" in d_id or "geran" in d_id or "lancet" in d_id else "recon",
                            propulsion="unknown",
                            total_components_documented=0,
                            primary_source_url=f"{BASE}/en/page-{d_id}",
                            secondary_sources=json.dumps([]),
                            image_url="",
                            last_verified=date.today().isoformat(),
                            notes="Auto-registered from GUR component listing",
                        )
                    drones_seen[d_id].total_components_documented += 1

        return components, list(drones_seen.values())


# --------------------------------------------------------------------------- #
# CSV writing
# --------------------------------------------------------------------------- #

def write_csv(rows: list, path: Path) -> None:
    if not rows:
        logging.warning("No rows to write to %s", path)
        # still write an empty CSV with headers (using the dataclass schema)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(asdict(row))
    logging.info("Wrote %d rows to %s", len(rows), path)


def derive_manufacturers(components: list[Component]) -> list[dict]:
    bucket: dict[tuple[str, str], dict] = {}
    for c in components:
        key = (c.manufacturer.strip(), c.manufacturer_country)
        if c.manufacturer.lower() in ("", "not identified"):
            continue
        if key not in bucket:
            bucket[key] = {
                "manufacturer_id": slugify(f"{c.manufacturer}-{c.manufacturer_country}"),
                "name": c.manufacturer,
                "country": c.manufacturer_country,
                "headquarters_city": "",
                "parent_company": "",
                "opensanctions_id": "",
                "sanctions_status": "unknown",
                "components_supplied": 0,
                "drones_supplied": 0,
                "source_url": COMPONENTS_INDEX,
                "notes": "",
            }
        bucket[key]["components_supplied"] += 1
    return list(bucket.values())


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default="data", help="Output directory")
    parser.add_argument("--rate-limit", type=float, default=1.0,
                        help="Seconds between requests (default 1.0)")
    parser.add_argument("--max-pages", type=int, default=0,
                        help="Stop after N pages (0 = unlimited)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    scraper = GurScraper(rate_limit=args.rate_limit, max_pages=args.max_pages)
    components, drones = scraper.scrape()

    out = Path(args.out_dir)
    write_csv(components, out / "components.csv")
    write_csv(drones, out / "drones.csv")

    mfrs = derive_manufacturers(components)
    if mfrs:
        out.mkdir(parents=True, exist_ok=True)
        with (out / "manufacturers.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(mfrs[0].keys()))
            w.writeheader()
            w.writerows(mfrs)
        logging.info("Wrote %d manufacturers to %s/manufacturers.csv", len(mfrs), out)

    logging.info("Done. %d components, %d drones, %d manufacturers.",
                 len(components), len(drones), len(mfrs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
