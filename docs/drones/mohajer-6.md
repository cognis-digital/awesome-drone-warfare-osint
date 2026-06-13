# Mohajer-6

> Iranian medium-altitude long-endurance (MALE) UAV manufactured by
> Qods Aviation Industries. Used by Russia after Iranian transfer.
> Heavily reliant on Western engine and electronics.

| | |
|---|---|
| **Slug** | `uav-mohajer-6` |
| **Operators** | 🇮🇷 IR (origin) · 🇷🇺 RU · 🇻🇪 VE (export) |
| **Role** | ISTAR + light strike (up to 4 hardpoints) |
| **Propulsion** | 🇨🇦/🇦🇹 **Rotax 912 IS Sport** (~100 hp) — same engine class as Bayraktar TB2 |
| **Sources** | [Iran Primer](https://iranprimer.usip.org/blog/2023/mar/01/explainer-american-parts-iranian-drones) · [ISIS-online](https://isis-online.org/isis-reports/iranian-drones-in-ukraine-contain-western-brand-components) · [TWZ](https://www.twz.com/rotax-engine-found-in-iranian-mohajer-6-drone-downed-over-ukraine) |

## Key forensic findings

The **Rotax 912 IS Sport** engine (BRP-Rotax, Austrian subsidiary of
Canadian BRP) is the same engine widely used in light sport aircraft.
Its delivery to Iran violated EU sanctions on dual-use exports —
documented by [Iran International](https://www.iranintl.com/en/202301147297).

Per Ukraine GUR's October 2022 teardown:
> "**3/4 of Mohajer-6 components are made in the US.** Rotex [sic]
> engine is obviously made in Canada and Austria. Other components
> are made in China and Japan."

This is the same ~75 % Western-origin profile observed across the
broader Iranian/Russian drone fleet — a baseline finding the dataset
records, traceable to specific GUR rows in `data/components.csv`.

## Cross-reference

- See [Mohajer-6 forensic page on GUR](https://war-sanctions.gur.gov.ua/en/components) (filter Armament = "UAV Mohajer-6")
- The Mohajer-6 supply chain partially overlaps with [Bayraktar TB2](https://en.wikipedia.org/wiki/Baykar_Bayraktar_TB2) (also uses Rotax engines + L3Harris/Wescam optics)
