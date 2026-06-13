# Awesome Drone Warfare OSINT — docs

This site (built from the `docs/` folder via MkDocs / GitHub Pages) hosts
the human-readable companion to the machine-readable dataset in
[`data/`](https://github.com/cognis-digital/awesome-drone-warfare-osint/tree/main/data).

## Quick links

- [README & headline numbers](https://github.com/cognis-digital/awesome-drone-warfare-osint#-the-dataset-at-a-glance)
- [Drone platforms](drones/index.md)
- [Components by category](components/index.md)
- [Theaters](theaters/index.md)
- [Playbooks (EW, counter-UAS)](playbooks/index.md)
- [Primary sources](sources.md)

## Dataset map

```mermaid
graph LR
  GUR[GUR War & Sanctions<br/>5,800+ components]
  NACP[NACP Trap.org.ua]
  CAR[Conflict Armament Research]
  IISS[IISS 2025 report]
  RUSI[RUSI Orlan Complex]
  KSE[KSE Institute]
  ISIS[ISIS-online]

  GUR --> COMP[(components.csv)]
  NACP --> COMP
  CAR --> TEAR[(teardowns.csv)]
  IISS --> TEAR
  RUSI --> EDGES[(supply_chain_edges.csv)]
  KSE --> ANALYSIS[(analysis notebooks)]
  ISIS --> COMP

  COMP --> DRONES[(drones.csv)]
  COMP --> MFG[(manufacturers.csv)]
  EDGES --> GRAPH[supply-chain graph]
```
