# Architecture

This document describes how the repository is put together: the data model, the
code layers, and the invariants that keep the two in sync.

## Layers

```
                 primary sources (GUR · NACP · CAR · institute reports)
                                     │  scrapers/*.py
                                     ▼
        ┌───────────────────────── data/ ─────────────────────────┐
        │  components.csv  drones.csv  manufacturers.csv           │
        │  teardowns.csv   supply_chain_edges.csv  incidents.csv   │
        │  schemas/*.json  (JSON Schema, Draft 2020-12)            │
        └──────────────────────────┬──────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
 scripts/validate.py        osint_analytics.py            livesearch.py
 (schema + xref gate)       (pure analytics fns)          (keyless feeds)
                                    │
                                    ▼
                                 query.py
                        (CLI: search + analytics,
                         table / json / csv output)
```

### `data/` — the dataset

Six CSV tables, each with a matching JSON Schema in `data/schemas/`:

| Table | Grain | Key columns |
|---|---|---|
| `components` | one part *per platform it is documented in* | `component_id`, `manufacturer_country`, `sanctions_status`, `found_in_drones` (JSON list) |
| `drones` | one platform | `id`, `role`, `manufacturer_country`, `operators` (JSON list) |
| `manufacturers` | one maker | `manufacturer_id`, `country`, `sanctions_status` |
| `teardowns` | one forensic report | `teardown_id`, `drone_id`, `url` |
| `supply_chain_edges` | one relationship | `source_entity`, `target_entity`, `relation` |
| `incidents` | one geo-tagged strike (join-only) | `incident_id`, `lat`, `lon`, `drone_id` |

Multi-valued fields (`found_in_drones`, `operators`, `guidance`, …) are stored as
a JSON-encoded array inside a single CSV cell. Note that `component_id` is **not**
globally unique: the same catalogued part is listed once per platform it appears
in, which is what makes per-platform roll-ups cheap.

### `osint_analytics.py` — pure analytics

Side-effect-free, standard-library-only functions that operate on the
`list[dict]` rows produced by `csv.DictReader`:

* `parse_json_list(cell)` — safe decode of a JSON-list cell (never raises).
* `country_breakdown(components, drone_id=None)` — components per manufacturer
  country, optionally scoped to one platform (supply-chain **concentration**).
* `platform_exposure(components, country)` — components-from-`country` per
  platform (supplier **leverage**).
* `sanctions_breakdown(components, country=None)` — counts per `sanctions_status`.
* `to_csv(rows, cols)` — RFC-4180 CSV rendering for the `--format csv` path.
* `load_table(data_dir, name)` — the one intentional I/O helper.

Keeping these pure is deliberate: the CLI is a thin shell over them, so every
analytical result is exercised directly in `tests/test_osint_analytics.py`
against small in-memory fixtures, and end-to-end in `tests/test_query_cli.py`.

### `query.py` — the CLI

A `argparse` front end. It loads the relevant CSV, calls into
`osint_analytics`, and renders the result. Output format is resolved once by
`_fmt(args)`: an explicit `--format` wins, the legacy `--json` flag maps to
`json`, and the default is the human-readable `table`. `--selftest` runs a
dependency-free smoke check used by CI.

### `livesearch.py` — keyless live ingestion

Standard-library real-time ingestion (RSS/Atom parsing, a Google-News-RSS
search backend, a DuckDuckGo HTML fallback, and a `harvest()` mixer that
de-dupes by link and filters by recency/minimum-year). No API keys, no
third-party dependencies.

### `scripts/validate.py` — the CI gate

Validates every row against its JSON Schema (coercing CSV strings into the
JSON types the schema expects) and checks cross-table referential integrity.
Exits non-zero on failure so bad PRs are caught.

## Invariants

* Every component row carries a public `source_url` (provenance rule, enforced
  in review/CI).
* `manufacturer_country` matches `^([A-Z]{2}|UNK)$`.
* `sanctions_status` is drawn from a fixed vocabulary.
* `found_in_drones` is always a non-empty JSON list.
* The overwhelming majority of referenced platforms resolve to a row in
  `drones.csv` (stubs are auto-registered by the scrapers).

These are asserted both by `scripts/validate.py` (per-row, schema) and by
`tests/test_data_integrity.py` (cross-row, in pytest).
