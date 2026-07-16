# Usage

`query.py` is pure standard library — clone the repo and run it with any
Python 3.9+. Nothing to install for querying.

```bash
python query.py <command> [args] [--format {table,json,csv}]
```

`--format` (and its shorthand `--json`) is a **global** flag: put it before the
subcommand, e.g. `python query.py --json stats`.

## Commands

### `component <text>`

Full-text search over component name/marking, manufacturer, and OEM part number.

```bash
python query.py component jetson
python query.py component "STM32F103"
python query.py --json component u-blox
```

### `manufacturer <text>`

Every documented component from manufacturers matching `<text>`, plus the set of
platforms those parts appear in.

```bash
python query.py manufacturer "Texas Instruments"
python query.py manufacturer u-blox
```

### `country <CC>`

Components whose manufacturer country is `<CC>` (ISO-3166 alpha-2, case
insensitive). Table output is capped at 200 rows; use `--format json`/`csv` for
the full set.

```bash
python query.py country US
python query.py --format csv country CH > swiss_parts.csv
```

### `drone <id>`

Components documented inside a single platform.

```bash
python query.py drone shahed-136-uav-157-components
python query.py drone geran-4-uav
```

### `drones [--operator RU] [--role loitering] [--country IR]`

List platforms, optionally filtered. `--operator` matches an operator code in the
platform's `operators` list; `--role` and `--country` are substring / exact-code
matches respectively.

```bash
python query.py drones --operator RU --role loitering_munition
python query.py --json drones --country IR
```

### `chokepoint <drone_id>` — supply-chain concentration

Breaks a platform's documented components down by manufacturer country and reports
each origin's share of the total. Surfaces single-origin choke points.

```bash
$ python query.py chokepoint geran-4-uav
  country  components  share_pct
  US       24          44.4
  CN       14          25.9
  UNK      10          18.5
  DE       2           3.7
  ...
  54 component(s) across 7 origin countries for 'geran-4-uav'.
  Most concentrated origin: US (24, 44.4%).
```

### `exposure <CC>` — supplier leverage

The mirror image of `chokepoint`: for a manufacturer country, how many of its
parts appear in each platform. A high count means the platform is heavily
dependent on that country's supply.

```bash
$ python query.py exposure US
  drone                          components_from_country
  uav-shahed-131                 1951
  corsair-uav                    138
  ...
```

### `sanctions [--country CC]` — sanctions posture

Component breakdown by `sanctions_status`, optionally scoped to one origin
country.

```bash
python query.py sanctions
python query.py sanctions --country CN
python query.py --format csv sanctions > sanctions_posture.csv
```

### `stats` — headline numbers

```bash
python query.py stats
python query.py --json stats
python query.py --format csv stats   # top country origins as CSV
```

### `--selftest`

Dependency-free smoke test (used by CI): loads the CSVs and checks basic
structure. Prints `[OK] query selftest passed`.

```bash
python query.py --selftest
```

## Live search (`livesearch.py`)

Keyless, standard-library real-time ingestion. Useful for monitoring new OSINT on
a platform or component.

```bash
python -m livesearch "shahed drone components" --when 7d --json
python -m livesearch --feed https://example.org/rss.xml
python -m livesearch "sanctions evasion microchips" --ddg
```

Programmatic:

```python
from livesearch import web_search, harvest

items = web_search("kh-101 foreign components", when="30d")
mixed = harvest([
    {"query": "iran drone engine sanctions", "when": "7d"},
    "https://someorg.example/feed.xml",
], since_days=14, min_year=2026)
```

## Exit codes

`query.py` returns `0` on success. Argument errors exit `2` (argparse). The
validator (`scripts/validate.py`) exits non-zero when any row fails.
