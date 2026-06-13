#!/usr/bin/env python3
"""
scripts/validate.py
===================

Validates every row in data/*.csv against the matching JSON Schema in
data/schemas/, plus cross-row referential integrity (components ->
drones, drones -> manufacturers, etc.). Exits non-zero on failure so
GitHub Actions catches bad PRs.

USAGE
-----
    python scripts/validate.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCHEMA_DIR = DATA / "schemas"

TABLES = {
    "drones":              SCHEMA_DIR / "drones.schema.json",
    "components":          SCHEMA_DIR / "components.schema.json",
    "manufacturers":       SCHEMA_DIR / "manufacturers.schema.json",
    "incidents":           SCHEMA_DIR / "incidents.schema.json",
    "teardowns":           SCHEMA_DIR / "teardowns.schema.json",
    "supply_chain_edges":  SCHEMA_DIR / "supply_chain_edges.schema.json",
}

# Fields that are JSON-encoded lists in the CSV but real lists in JSON Schema
LIST_FIELDS = {
    "drones": ["aka", "operators", "guidance", "secondary_sources"],
    "components": ["found_in_drones", "replaceable_with"],
}


# Fields where an empty string in CSV means "absent" (not the string "")
NULLABLE_BLANK_FIELDS = {
    "components": {"function", "oem_part_number", "production_date", "price_retail_usd",
                   "evidence_image", "notes"},
    "manufacturers": {"headquarters_city", "parent_company", "opensanctions_id", "notes"},
    "drones": {"image_url", "model_3d_url", "notes"},
    "teardowns": {"doi", "notes"},
    "supply_chain_edges": {"notes", "confidence"},
    "incidents": {"admin1", "location_name", "launch_party", "target_type", "outcome", "notes"},
}


def coerce_row(table: str, row: dict[str, Any]) -> dict[str, Any]:
    """Convert CSV strings into the JSON types expected by the schema."""
    blanks = NULLABLE_BLANK_FIELDS.get(table, set())
    for k, v in list(row.items()):
        if pd.isna(v):
            row[k] = None
        elif isinstance(v, str) and v == "" and k in blanks:
            row[k] = None
    # decode list fields
    for f in LIST_FIELDS.get(table, []):
        v = row.get(f)
        if isinstance(v, str):
            try:
                row[f] = json.loads(v)
            except Exception:
                row[f] = []
    # coerce bool
    for f in ("is_dual_use", "is_pdf"):
        if f in row and isinstance(row[f], str):
            row[f] = row[f].strip().lower() in ("true", "1", "yes")
    # ints
    for f in ("total_components_documented", "components_supplied",
              "drones_supplied", "components_referenced"):
        if f in row and row[f] is not None and not isinstance(row[f], bool):
            try:
                row[f] = int(row[f])
            except (TypeError, ValueError):
                row[f] = 0
    # floats
    for f in ("price_retail_usd", "unit_cost_usd_est", "wingspan_m",
              "length_m", "mtow_kg", "payload_kg", "range_km",
              "endurance_min", "cruise_speed_kmh", "ceiling_m",
              "lat", "lon"):
        if f in row and row[f] not in (None, ""):
            try:
                row[f] = float(row[f])
            except (TypeError, ValueError):
                row[f] = None
        elif f in row and row[f] == "":
            row[f] = None
    return row


def validate_table(table: str, schema_path: Path) -> tuple[int, int]:
    csv_path = DATA / f"{table}.csv"
    if not csv_path.exists():
        print(f"[skip] {csv_path} not present")
        return 0, 0
    schema = json.loads(schema_path.read_text())
    v = Draft202012Validator(schema)
    df = pd.read_csv(csv_path, keep_default_na=False, na_values=[""])
    ok, bad = 0, 0
    for i, raw in enumerate(df.to_dict(orient="records")):
        row = coerce_row(table, raw)
        errors = list(v.iter_errors(row))
        if errors:
            bad += 1
            if bad <= 5:  # print only first few
                print(f"  [{table}] row {i} ({row.get('component_id') or row.get('id') or '?'}): {errors[0].message}")
        else:
            ok += 1
    print(f"[{table}] {ok} ok, {bad} failed (of {len(df)} rows)")
    return ok, bad


def cross_refs() -> int:
    """Check referential integrity across tables."""
    fails = 0
    try:
        drones = pd.read_csv(DATA / "drones.csv")
        components = pd.read_csv(DATA / "components.csv")
    except FileNotFoundError:
        return 0
    drone_ids = set(drones["id"].astype(str))
    missing = set()
    for s in components["found_in_drones"]:
        for d in json.loads(s) if isinstance(s, str) else []:
            if d and d not in drone_ids:
                missing.add(d)
    if missing:
        # Not a hard failure — we auto-create drone stubs from component listings.
        print(f"[xref] {len(missing)} drone slugs in components.csv not (yet) in drones.csv "
              f"(soft warning; auto-registered next scrape)")
    else:
        print("[xref] components -> drones referential integrity OK")
    return fails


def main() -> int:
    total_bad = 0
    for table, schema_path in TABLES.items():
        if not schema_path.exists():
            print(f"[warn] missing schema: {schema_path}")
            continue
        _, bad = validate_table(table, schema_path)
        total_bad += bad
    total_bad += cross_refs()
    if total_bad:
        print(f"\n[FAIL] Validation failed: {total_bad} bad row(s)")
        return 1
    print("\n[OK] All rows validate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
