# Scrapers

| Script | Source | Notes |
|---|---|---|
| `gur_war_sanctions.py` | GUR/HUR Components portal | Primary data feed, rate-limited 1 req/s |
| `nacp_sanctions.py` | Trap.org.ua (NACP) | Stub — implement against live portal |
| `car_field_dispatches.py` | Conflict Armament Research | Indexes report URLs only — never redistributes report content |

## Etiquette

All scrapers in this directory follow the same rules:

1. **One request per second** by default (`--rate-limit 1.0`).
2. **Respect `robots.txt`**.
3. **Identifying `User-Agent`** with a contact URL.
4. **Fail-fast on 4xx** — never retry-hammer.
5. **Resume from last page** — every page write is atomic.

## Running

```bash
pip install -r ../requirements.txt
python gur_war_sanctions.py --out-dir ../data/ --rate-limit 1.0
python car_field_dispatches.py --out-dir ../data/
```

## CI cadence

The repo includes `.github/workflows/update-data.yml`, which runs every
Monday at 06:00 UTC, runs all scrapers, and opens a PR with the diff.
