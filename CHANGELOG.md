# Changelog

## [0.4.0] — 2026-06-13
### Added
- `docs/counter-uas-detection.md` — a defensive reference on how hostile drones are
  detected/classified/identified (RF, radar micro-Doppler, acoustic, EO/IR sensor
  fusion; DJI DroneID/OcuSync, RF fingerprinting), the descriptive C-UAS effector
  landscape (EW, HPM/THOR/Leonidas, lasers, interceptors), and the governing standards
  (FAA Remote ID, ASTM F3411 + its spoofing caveat, CISA/CRS/Army/NIST). Cited; strictly
  detection/identification/analysis — no control/targeting/defeat procedures.
- README quick-link to the counter-UAS reference.

## [0.3.0] — 2026-06-13
### Added
- `docs/STATISTICS.md` — "what worked / what didn't" by the numbers: cited
  2022–2026 figures on drone effectiveness, electronic warfare, counter-UAS, and
  the foreign-component supply chain, each linked to its primary/secondary source
  (CSIS, GUR War & Sanctions, CAR, US Senate HSGAC, Epirus, MarketsandMarkets, …).
- Quick-link to the statistics page from the README.

### Fixed
- `scripts/validate.py` no longer crashes on Windows consoles (cp1252): replaced
  the unicode status glyphs with ASCII `[OK]`/`[FAIL]` so validation runs and
  exits 0 cross-platform. Dataset currently validates: 195 drones, 8,326
  components, 621 manufacturers, 31 teardowns, 28 supply-chain edges.

### Changed
- Repository owner placeholders (`USER`) resolved to `cognis-digital`.

## [0.2.0] — 2026-06-12
- Initial public dataset: schemas, drones/manufacturers/components/teardowns/
  supply-chain tables, per-system docs, analytical playbooks, CI validation.
