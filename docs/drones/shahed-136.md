# Shahed-136 / Geran-2 (MS001)

> Iranian-designed, Russian-produced single-use loitering munition.
> The single most-documented drone in the corpus.

| | |
|---|---|
| **Slug** | `shahed-136-geran-2-ms001` |
| **Operators** | 🇷🇺 RU (as "Geran-2"), 🇮🇷 IR (origin) |
| **Role** | Loitering munition |
| **Propulsion** | MADO MD550 piston engine (Iran) |
| **Wingspan** | ~2.5 m (delta) |
| **Documented foreign components** | 75 (primary), 157 (variant) |
| **Primary source** | <https://war-sanctions.gur.gov.ua/en/page-shahed-136> |

## Cost & physical description

> "An Iranian-made Shahed-136 drone is a simple weapon. The delta wings, which
> span 2.5 meters, are made of fiberglass and end in two fixed vertical fins…"
> — [Phenomenal World, Drones Like Bicycles](https://phenomenalworld.org/analysis/cost-of-a-shahed/)

## Notable components (from GUR forensic record)

| Component | Marking | Manufacturer | Country |
|---|---|---|---|
| Piston engine | MD550 | MADO | 🇮🇷 IR |
| Rail-to-rail buffer | MAX4222 | Maxim / Analog Devices | 🇺🇸 US |
| DSP | TMS320F28335 | Texas Instruments | 🇺🇸 US |
| FPGA config PROM | XCF16P | Xilinx (AMD) | 🇺🇸 US |
| Flash memory | AM29LV033C | AMD | 🇺🇸 US |
| Digital isolator | I7420F | Texas Instruments | 🇺🇸 US |
| RS-485 transceiver | MAX3486 | Maxim / Analog Devices | 🇺🇸 US |
| DC/DC converter | MCW03-24S12 | Minmax | 🇹🇼 TW |
| DC/DC converter | MJWI20-24S05 | Minmax | 🇹🇼 TW |
| SD/HD video encoder | (Analog Devices part) | Analog Devices | 🇺🇸 US |
| Memory chip | XCF16P FG48 | Xilinx (AMD) | 🇺🇸 US |
| Video capture | EZCAP USB3.0 AHD | Shenzhen ForwardVideo | 🇨🇳 CN |

Full programmatic listing: filter `components.csv` where
`found_in_drones` contains `shahed-136-geran-2-ms001`.

## Secondary sources

- [IISS 2025 — Tracking the Components of Missiles and UAVs Used by Russia in Ukraine](https://www.iiss.org/globalassets/media-library---content--migration/files/research-papers/2025/09/pub25-094-tracking-the-components-of-missiles-and-uavs-used-by-russia-in-ukraine.pdf)
- [KSE Institute — Foreign Components in Russian Military Drones](https://kse.ua/about-the-school/news/foreign-components-in-russian-military-drones/)
- [Conflict Armament Research — Documenting the domestic Russian variant of the Shahed UAV](https://storymaps.arcgis.com/stories/d3be20c31acd4112b0aecece5b2a283c)
- [SwissInfo — Russia's killer drones still boast Swiss components](https://www.swissinfo.ch/eng/business/russia-s-killer-drones-still-boast-swiss-components-how-come/48940138)
- [OSMP.ngo — Shahed-131 & -136 UAVs: a visual guide](https://osmp.ngo/collection/shahed-131-136-uavs-a-visual-guide/)
