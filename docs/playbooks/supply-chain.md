# Supply-chain & sanctions-evasion playbook

> This page summarizes the **how** of getting Western semiconductors
> into Russian drones, as documented in published investigations.
> It is purely descriptive and aims to help analysts, regulators,
> and compliance teams identify red flags.

## The macro picture

* **~70 %** of Western-branded parts in Russian drones are **genuine**,
  originally exported legally to global markets ([CEPA](https://cepa.org/article/western-chips-power-russias-war/)).
* **~30 %** are grey-market: contract-fab over-production ("ghost shifts"),
  counterfeits, or pulled from white goods (dishwashers, refrigerators)
  imported through Central Asia ([re-russia.net](https://re-russia.net/en/review/164/)).
* China supplies **~67 %** of shipments ([B4Ukraine](https://b4ukraine.org/whats-new/russian-drones)),
  with **~17 %** routed through **Hong Kong**.
* US-origin semiconductors account for the largest share by manufacturer
  (Texas Instruments, Analog Devices, Intel/Altera, Xilinx/AMD).

## The transit hubs

| Hub | Role |
|---|---|
| 🇨🇳 **Shenzhen** | Mass production + Minghuaxin-class distributors ([Leave-Russia](https://leave-russia.org/shenzhen-minghuaxin)) |
| 🇭🇰 **Hong Kong** | Shell-company relay ([ICIJ](https://www.icij.org/news/2026/02/hong-kong-firms-feed-european-tech-to-russias-war-in-ukraine-report-says/), [CFHK](https://thecfhk.org/research/europe-sanctions-evasion/)) |
| 🇦🇪 **UAE** | Re-export ([EvidenCity](https://www.evidencity.com/how-russian-companies-circumvent-sanctions-through-turkey-and-the-uae)) |
| 🇹🇷 **Turkey** | Re-export + dual-use front companies |
| 🇰🇿 **Kazakhstan** | Central Asian whack-a-mole ([CEPA](https://cepa.org/article/central-asian-whack-a-mole-western-tech-evades-sanctions-feeds-russian-war-machine/)) |
| 🇰🇬 **Kyrgyzstan** | Similar to KZ |
| 🇦🇲 **Armenia** | Similar to KZ |

## Procurement tradecraft (publicly documented)

* **One-day shell companies** — incorporated, used once, dissolved
* **Customs misclassification** — HS codes deliberately wrong
* **Multi-leg shipping** — EU → KZ → CN → RU sequence
* **White-goods diversion** — chip-harvesting from imported appliances
* **"Brokerage" agents** in Brooklyn, Brno, Dubai, Almaty (per [DOJ indictments](https://www.bis.gov/press-release/brooklyn-resident-two-russian-nationals-charged-exporting-dual-use-electronics-used-russian-militarys))

## Notable producer-side responses

| Vendor | Action |
|---|---|
| **u-blox** | Banned use of GNSS modules in war 🇺🇦/🇷🇺 (Dec 2024) — [GPS World](https://www.gpsworld.com/u-blox-bans-the-use-of-its-gnss-modules-in-war/) |
| **Analog Devices** | Reduced Russian operations — [Leave-Russia](https://leave-russia.org/analog-devices) |
| **STMicroelectronics** | Statement Feb 2023 — [B4Ukraine](https://b4ukraine.org/pdf/STM.pdf) |
| **TI / AMD / Intel / ADI** | Identified & blocked entities since 2024 ([HSGAC report PDF](https://www.hsgac.senate.gov/wp-content/uploads/09.10.2024-Majority-Staff-Report-The-U.S.-Technology-Fueling-Russias-War-in-Ukraine.pdf)) |

## Recommended controls (per CEPA / HSGAC)

1. **Real-time forensic database** of part numbers found in Russian
   weapons → flag for licensing.
2. **Transatlantic task force** focused on KZ/KG/AM/TR/AE traders.
3. **KYC for distributors** — harmonized rules.
4. **Cryptographic provenance** for high-risk part families.
5. **Bulk-order anomaly detection** by e-commerce / payment platforms.
6. **Hardened white-goods PCBs** that resist chip salvage.

## See also

- [`docs/sources.md`](../sources.md) — primary source index
- [`data/supply_chain_edges.csv`](../../data/supply_chain_edges.csv) — graph data
- [OpenSanctions](https://www.opensanctions.org/countries/ru/) (310k+ Russia-linked entities)
