#!/usr/bin/env python3
"""Query the drone-warfare OSINT dataset — for analysts, OSINT teams, and
export-control / sanctions-compliance work. Pure standard library.

The dataset answers a question compliance teams actually have:
  "Does a part we (or a supplier) make show up in any documented weapon system?"

Commands:
  component <text>     search components by name / part-number / manufacturer
  manufacturer <text>  every documented component from a manufacturer + which drones
  country <CC>         components by manufacturer country (e.g. US, CH, CN)
  drone <id>           components documented in a drone
  drones [filters]     list drone/missile platforms (--operator/--role/--country)
  stats                headline dataset numbers
Add --json for machine-readable output.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")


def _load(name: str) -> list[dict]:
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _jlist(s: str) -> list:
    try:
        v = json.loads(s or "[]")
        return v if isinstance(v, list) else []
    except json.JSONDecodeError:
        return []


def _emit(rows: list[dict], cols: list[str], as_json: bool) -> None:
    if as_json:
        print(json.dumps(rows, indent=2)); return
    if not rows:
        print("  (no matches)"); return
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    print("  " + "  ".join(c.ljust(widths[c]) for c in cols))
    for r in rows:
        print("  " + "  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


def cmd_component(args) -> int:
    q = args.text.lower()
    comps = _load("components.csv")
    hits = [c for c in comps if q in (c["name_marking"] + c["manufacturer"]
            + c["oem_part_number"]).lower()]
    rows = [{"component_id": c["component_id"], "name": c["name_marking"],
             "manufacturer": c["manufacturer"], "country": c["manufacturer_country"],
             "part": c["oem_part_number"], "sanctions": c["sanctions_status"],
             "found_in": ", ".join(_jlist(c["found_in_drones"]))} for c in hits]
    _emit(rows, ["component_id", "name", "manufacturer", "country", "found_in"], args.json)
    if not args.json:
        print(f"\n  {len(rows)} component(s) match '{args.text}'.")
    return 0


def cmd_manufacturer(args) -> int:
    q = args.text.lower()
    comps = [c for c in _load("components.csv") if q in c["manufacturer"].lower()]
    drones: set[str] = set()
    for c in comps:
        drones.update(_jlist(c["found_in_drones"]))
    rows = [{"component_id": c["component_id"], "name": c["name_marking"],
             "country": c["manufacturer_country"],
             "found_in": ", ".join(_jlist(c["found_in_drones"]))} for c in comps]
    _emit(rows, ["component_id", "name", "country", "found_in"], args.json)
    if not args.json:
        print(f"\n  {len(comps)} component(s) from manufacturers matching '{args.text}', "
              f"documented across {len(drones)} drone/weapon type(s): {', '.join(sorted(drones)) or '—'}")
    return 0


def cmd_country(args) -> int:
    cc = args.cc.upper()
    comps = [c for c in _load("components.csv") if c["manufacturer_country"].upper() == cc]
    rows = [{"component_id": c["component_id"], "name": c["name_marking"],
             "manufacturer": c["manufacturer"], "found_in": ", ".join(_jlist(c["found_in_drones"]))}
            for c in comps]
    _emit(rows[:200], ["component_id", "name", "manufacturer", "found_in"], args.json)
    if not args.json:
        print(f"\n  {len(comps)} component(s) with manufacturer country {cc} "
              f"(showing up to 200).")
    return 0


def cmd_drone(args) -> int:
    comps = [c for c in _load("components.csv") if args.id in _jlist(c["found_in_drones"])]
    rows = [{"component_id": c["component_id"], "name": c["name_marking"],
             "manufacturer": c["manufacturer"], "country": c["manufacturer_country"]} for c in comps]
    _emit(rows, ["component_id", "name", "manufacturer", "country"], args.json)
    if not args.json:
        print(f"\n  {len(comps)} component(s) documented in '{args.id}'.")
    return 0


def cmd_drones(args) -> int:
    ds = _load("drones.csv")
    if args.role:
        ds = [d for d in ds if args.role.lower() in d["role"].lower()]
    if args.country:
        ds = [d for d in ds if d["manufacturer_country"].upper() == args.country.upper()]
    if args.operator:
        ds = [d for d in ds if args.operator.upper() in [o.upper() for o in _jlist(d["operators"])]]
    rows = [{"id": d["id"], "name": d["display_name"], "role": d["role"],
             "country": d["manufacturer_country"], "components": d["total_components_documented"]}
            for d in ds]
    _emit(rows, ["id", "name", "role", "country", "components"], args.json)
    if not args.json:
        print(f"\n  {len(rows)} platform(s).")
    return 0


def cmd_stats(args) -> int:
    comps, drones = _load("components.csv"), _load("drones.csv")
    by_country: dict[str, int] = {}
    for c in comps:
        by_country[c["manufacturer_country"]] = by_country.get(c["manufacturer_country"], 0) + 1
    top = sorted(by_country.items(), key=lambda kv: kv[1], reverse=True)[:10]
    out = {"drones": len(drones), "components": len(comps),
           "manufacturers": len({c["manufacturer"] for c in comps}),
           "top_manufacturer_countries": top}
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"  drones/platforms: {out['drones']}\n  components: {out['components']}\n"
              f"  distinct manufacturers: {out['manufacturers']}")
        print("  top component manufacturer countries:")
        for cc, n in top:
            print(f"    {cc or 'UNK':6s} {n}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="query", description=__doc__.splitlines()[0])
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("component"); s.add_argument("text"); s.set_defaults(fn=cmd_component)
    s = sub.add_parser("manufacturer"); s.add_argument("text"); s.set_defaults(fn=cmd_manufacturer)
    s = sub.add_parser("country"); s.add_argument("cc"); s.set_defaults(fn=cmd_country)
    s = sub.add_parser("drone"); s.add_argument("id"); s.set_defaults(fn=cmd_drone)
    s = sub.add_parser("drones")
    s.add_argument("--operator"); s.add_argument("--role"); s.add_argument("--country")
    s.set_defaults(fn=cmd_drones)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    return p


def selftest() -> int:
    """Non-interactive checks for CI."""
    comps = _load("components.csv")
    assert comps and "found_in_drones" in comps[0]
    # the JSON list field parses
    assert isinstance(_jlist(comps[0]["found_in_drones"]), list)
    drones = _load("drones.csv")
    assert drones and "id" in drones[0]
    print("[OK] query selftest passed")
    return 0


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
