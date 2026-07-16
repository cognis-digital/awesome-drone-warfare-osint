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
  chokepoint <id>      supply-chain concentration for a platform (parts by country)
  exposure <CC>        which platforms depend on a country's parts (supplier leverage)
  sanctions [--country CC]  component breakdown by sanctions status
  stats                headline dataset numbers
Add --json (or --format json/csv/table) for machine-readable output.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys

from osint_analytics import (
    country_breakdown,
    parse_json_list,
    platform_exposure,
    sanctions_breakdown,
    to_csv,
)

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")


def _load(name: str) -> list[dict]:
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _jlist(s: str) -> list:
    # Retained for backward compatibility; delegates to the analytics module.
    return parse_json_list(s)


def _fmt(args) -> str:
    """Resolve the effective output format from the parsed arguments.

    ``--format`` wins when given; the legacy ``--json`` flag maps to
    ``json``; otherwise the default is the human-readable ``table``.
    """
    if getattr(args, "format", None):
        return args.format
    return "json" if getattr(args, "json", False) else "table"


def _emit(rows: list[dict], cols: list[str], fmt) -> None:
    """Render tabular ``rows`` in the requested format.

    ``fmt`` may be a format string ("table"/"json"/"csv") or, for backward
    compatibility, a truthy/falsey value where truthy means JSON.
    """
    if fmt is True:
        fmt = "json"
    elif fmt is False:
        fmt = "table"
    if fmt == "json":
        print(json.dumps(rows, indent=2)); return
    if fmt == "csv":
        sys.stdout.write(to_csv(rows, cols)); return
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
    fmt = _fmt(args)
    _emit(rows, ["component_id", "name", "manufacturer", "country", "found_in"], fmt)
    if fmt == "table":
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
    fmt = _fmt(args)
    _emit(rows, ["component_id", "name", "country", "found_in"], fmt)
    if fmt == "table":
        print(f"\n  {len(comps)} component(s) from manufacturers matching '{args.text}', "
              f"documented across {len(drones)} drone/weapon type(s): {', '.join(sorted(drones)) or '—'}")
    return 0


def cmd_country(args) -> int:
    cc = args.cc.upper()
    comps = [c for c in _load("components.csv") if c["manufacturer_country"].upper() == cc]
    rows = [{"component_id": c["component_id"], "name": c["name_marking"],
             "manufacturer": c["manufacturer"], "found_in": ", ".join(_jlist(c["found_in_drones"]))}
            for c in comps]
    fmt = _fmt(args)
    _emit(rows[:200], ["component_id", "name", "manufacturer", "found_in"], fmt)
    if fmt == "table":
        print(f"\n  {len(comps)} component(s) with manufacturer country {cc} "
              f"(showing up to 200).")
    return 0


def cmd_drone(args) -> int:
    comps = [c for c in _load("components.csv") if args.id in _jlist(c["found_in_drones"])]
    rows = [{"component_id": c["component_id"], "name": c["name_marking"],
             "manufacturer": c["manufacturer"], "country": c["manufacturer_country"]} for c in comps]
    fmt = _fmt(args)
    _emit(rows, ["component_id", "name", "manufacturer", "country"], fmt)
    if fmt == "table":
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
    fmt = _fmt(args)
    _emit(rows, ["id", "name", "role", "country", "components"], fmt)
    if fmt == "table":
        print(f"\n  {len(rows)} platform(s).")
    return 0


def cmd_chokepoint(args) -> int:
    """Supply-chain concentration: documented parts of a platform by country."""
    comps = _load("components.csv")
    breakdown = country_breakdown(comps, drone_id=args.id)
    total = sum(n for _, n in breakdown)
    rows = [{"country": cc, "components": n,
             "share_pct": f"{(100.0 * n / total):.1f}" if total else "0.0"}
            for cc, n in breakdown]
    fmt = _fmt(args)
    _emit(rows, ["country", "components", "share_pct"], fmt)
    if fmt == "table":
        if not total:
            print(f"\n  No components documented in '{args.id}'.")
        else:
            lead_cc, lead_n = breakdown[0]
            print(f"\n  {total} component(s) across {len(breakdown)} origin countries "
                  f"for '{args.id}'. Most concentrated origin: {lead_cc} "
                  f"({lead_n}, {100.0 * lead_n / total:.1f}%).")
    return 0


def cmd_exposure(args) -> int:
    """Supplier leverage: which platforms depend on a country's parts."""
    comps = _load("components.csv")
    exposure = platform_exposure(comps, args.cc)
    rows = [{"drone": d, "components_from_country": n} for d, n in exposure]
    fmt = _fmt(args)
    _emit(rows, ["drone", "components_from_country"], fmt)
    if fmt == "table":
        total = sum(n for _, n in exposure)
        print(f"\n  {args.cc.upper()} parts documented in {len(exposure)} platform(s) "
              f"({total} component-instances total).")
    return 0


def cmd_sanctions(args) -> int:
    """Component breakdown by sanctions status (optionally one country)."""
    comps = _load("components.csv")
    breakdown = sanctions_breakdown(comps, country=args.country)
    total = sum(n for _, n in breakdown)
    rows = [{"sanctions_status": s, "components": n,
             "share_pct": f"{(100.0 * n / total):.1f}" if total else "0.0"}
            for s, n in breakdown]
    fmt = _fmt(args)
    _emit(rows, ["sanctions_status", "components", "share_pct"], fmt)
    if fmt == "table":
        scope = f" from {args.country.upper()}" if args.country else ""
        print(f"\n  {total} component(s){scope} across "
              f"{len(breakdown)} sanctions status value(s).")
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
    fmt = _fmt(args)
    if fmt == "json":
        print(json.dumps(out, indent=2))
    elif fmt == "csv":
        sys.stdout.write(to_csv(
            [{"country": cc, "components": n} for cc, n in top],
            ["country", "components"]))
    else:
        print(f"  drones/platforms: {out['drones']}\n  components: {out['components']}\n"
              f"  distinct manufacturers: {out['manufacturers']}")
        print("  top component manufacturer countries:")
        for cc, n in top:
            print(f"    {cc or 'UNK':6s} {n}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="query", description=__doc__.splitlines()[0])
    p.add_argument("--json", action="store_true",
                   help="shorthand for --format json (kept for compatibility)")
    p.add_argument("--format", choices=("table", "json", "csv"),
                   help="output format (default: table)")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("component"); s.add_argument("text"); s.set_defaults(fn=cmd_component)
    s = sub.add_parser("manufacturer"); s.add_argument("text"); s.set_defaults(fn=cmd_manufacturer)
    s = sub.add_parser("country"); s.add_argument("cc"); s.set_defaults(fn=cmd_country)
    s = sub.add_parser("drone"); s.add_argument("id"); s.set_defaults(fn=cmd_drone)
    s = sub.add_parser("drones")
    s.add_argument("--operator"); s.add_argument("--role"); s.add_argument("--country")
    s.set_defaults(fn=cmd_drones)
    s = sub.add_parser("chokepoint"); s.add_argument("id"); s.set_defaults(fn=cmd_chokepoint)
    s = sub.add_parser("exposure"); s.add_argument("cc"); s.set_defaults(fn=cmd_exposure)
    s = sub.add_parser("sanctions"); s.add_argument("--country"); s.set_defaults(fn=cmd_sanctions)
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
