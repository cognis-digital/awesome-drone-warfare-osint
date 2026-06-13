# Dataset schemas

Every CSV in `data/` is validated against a JSON Schema (Draft 2020-12)
in this directory. CI runs `make validate` on every PR.

| Table | Schema | Description |
|---|---|---|
| `drones.csv` | `drones.schema.json` | One row per documented platform |
| `components.csv` | `components.schema.json` | One row per identified part |
| `manufacturers.csv` | `manufacturers.schema.json` | One row per company |
| `incidents.csv` | `incidents.schema.json` | Geo-tagged events |
| `teardowns.csv` | `teardowns.schema.json` | Links to forensic reports |
| `supply_chain_edges.csv` | `supply_chain_edges.schema.json` | Graph edges |

## Validation

```bash
pip install -r ../../requirements.txt
python -m scripts.validate
```

CI uses both **JSON Schema** (structural) and **Pandera** (cross-row, e.g.
"every `components.found_in_drones[*]` must exist as `drones.id`").
