# Baba-Yaga / Vampire heavy bomber family

> Russian nickname for a class of Ukrainian heavy multi-rotor bomber
> drones, typically operating at night with thermal optics. Vampire is
> one specific model in this family. Built on open-source ArduPilot
> autopilots and commercial off-the-shelf hardware.

| | |
|---|---|
| **Models** | Vampire, R18, plus dozens of cottage-built variants |
| **Operators** | 🇺🇦 UA. Some captured units now flown by 🇷🇺 RU per [Forbes (May 2026)](https://www.forbes.com/sites/vikrammittal/2026/05/23/captured-ukrainian-baba-yagas-are-becoming-russias-drone-of-choice/) |
| **Role** | Night bomber |
| **Propulsion** | Electric multi-rotor (octocopter typical, some hexa/quad) |
| **Payload** | Multiple bomblets / 122 mm shells |
| **Flight stack** | ArduPilot / PX4 derivatives |
| **Sources** | [Wikipedia](https://en.wikipedia.org/wiki/Baba_Yaga_(aircraft)) · [Ukrainian Arms Monitor](https://ukrainesarmsmonitor.substack.com/p/drone-warfare-in-ukraine-baba-yaga) |

## Why this family matters for the dataset

1. **Open-source autopilot lineage** — ArduPilot is canonical upstream; the
   Spider's Web operation used the same software stack ([CSIS](https://www.csis.org/analysis/how-ukraines-spider-web-operation-redefines-asymmetric-warfare)).
2. **Captured-and-reused** dynamic means Western and Chinese chips that
   originally entered through Ukraine's COTS supply chain end up in
   Russian-flown UAVs — a unique cross-front lineage.
3. The **mesh-networking shift** ([Ukrainian Arms Monitor](https://ukrainesarmsmonitor.substack.com/p/drone-warfare-in-ukraine-baba-yaga)) — Russia is replicating this design pattern with the Geran-4 in-band mesh modems.

## Components (open-source observations)

| Component | Vendor | Country |
|---|---|---|
| Flight controller | Pixhawk Cube (Hex) / Mateksys | 🇦🇺/🇨🇳 |
| Companion computer | Raspberry Pi 4/5 | 🇬🇧 UK |
| Motors | T-motor / Antigravity | 🇨🇳 CN |
| ESCs | Hobbywing / Mateksys | 🇨🇳 CN |
| GPS | u-blox NEO-M8N/F9P | 🇨🇭 CH |
| RC link | TBS Crossfire, ExpressLRS | 🇨🇿/open |
| Optics | Workswell Wiris / FLIR Boson | 🇨🇿/🇺🇸 |
| Battery | Tattu, custom Ukrainian | 🇨🇳/🇺🇦 |
