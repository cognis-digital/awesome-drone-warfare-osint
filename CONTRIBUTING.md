# Contributing

Thank you for considering a contribution. This dataset's value depends on
**rigorous sourcing**, so the bar for PRs is intentionally high — but the
process is short.

## TL;DR

```bash
git clone https://github.com/cognis-digital/awesome-drone-warfare-osint
cd awesome-drone-warfare-osint
pip install -r requirements.txt
make validate          # runs schema + provenance checks
git checkout -b add/geran-3-modem-variant
# … edit data/components.csv …
make validate
git commit -s -m "data(components): +47 rows from GUR Geran-3 page"
git push && gh pr create
```

The `-s` flag is required (Developer Certificate of Origin, see below).

## The four absolute rules

1. **Every row has a `source_url`.** It must be a public, archivable URL.
   PRs that add rows without `source_url` are auto-closed by CI.
2. **No firmware, no CAD, no exploit code, no jamming/spoofing recipes.**
   The repo is forensic, not operational. See [`DISCLAIMER.md`](DISCLAIMER.md).
3. **No personal data.** No operator names, no victim PII, no live coords
   of currently-deployed units.
4. **Same schema for all sides.** Russian and Ukrainian platforms use the
   identical schema. Methodological neutrality is non-negotiable.

## Schema

All schemas live under [`data/schemas/`](data/schemas/) as JSON Schema files.
The validator runs in CI; you can run it locally with `make validate`.

The core tables are:

- `drones.csv`        — one row per platform
- `components.csv`    — one row per identified part
- `manufacturers.csv` — one row per company
- `incidents.csv`     — one row per geo-tagged event
- `teardowns.csv`     — links to primary forensic reports
- `supply_chain_edges.csv` — graph edges

Field-level details are in [`data/schemas/README.md`](data/schemas/README.md).

## Issue templates

- **`new_drone.yml`** — propose a new platform
- **`new_component.yml`** — propose a new component row
- **`correction.yml`** — challenge an existing row (with evidence)
- **`takedown.yml`** — confidential take-down request (see DISCLAIMER)

## Code of Conduct

Be respectful. We follow the
[Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
Violations: open an issue tagged `code-of-conduct` or email the maintainers.

## Developer Certificate of Origin (DCO)

By signing your commit (`git commit -s`) you certify that you have the right
to submit the contribution under the repository's licenses (MIT for code,
CC BY 4.0 for data). Full DCO text: <https://developercertificate.org/>.

## Review checklist (auto-pasted into every PR)

```
- [ ] Every new/changed row has a working `source_url`
- [ ] Row passes JSON-Schema + Pandera validation (`make validate` is green)
- [ ] No firmware / CAD / exploit / jammer artefacts added
- [ ] No PII added
- [ ] If new manufacturer: cross-checked against OpenSanctions
- [ ] If new drone: docs/drones/<slug>.md stub added
- [ ] Commit signed (`-s`)
```

## "Good first row" contributions

Tag: [`good-first-row`](https://github.com/cognis-digital/awesome-drone-warfare-osint/labels/good-first-row)

Easy wins:
- Pick an under-documented platform from the GUR portal and add its 10–30
  most prominent components.
- Cross-link an existing component to a CAR field dispatch PDF.
- Add a manufacturer's `country_iso` + `opensanctions_id` if missing.
- Translate a `docs/drones/*.md` page into Ukrainian or another language.
