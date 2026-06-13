# Shahed-238

> Iranian jet-powered variant of the Shahed-136. Carries a turbojet
> instead of the MD550 piston engine, increasing speed and reducing
> intercept windows. Documented in Ukrainian wreckage.

| | |
|---|---|
| **Slug** | `shahed-238` |
| **Operators** | 🇷🇺 RU (Geran-3 variant), 🇮🇷 IR (origin) |
| **Role** | Loitering munition (high-speed long-range strike) |
| **Propulsion** | TEM **Tolou-10/13** turbojet — based on Czech PBS TJ100 design |
| **Sources** | [TWZ](https://www.twz.com/irans-jet-powered-shahed-drone-could-be-a-problem-for-ukraine) · [Militarnyi](https://militarnyi.com/en/news/czech-engine-and-western-electronics-components-of-the-shahed-238-drone-revealed/) · [OSMP](https://osmp.ngo/collection/shahed-131-136-uavs-a-visual-guide/) |

## Key technical findings

* The Shahed-238 retains the Shahed-136 airframe but replaces the piston
  engine with a turbojet.
* Per Defense Express, the engine appears to be the **TEM Tolou-10**, an
  Iranian copy of the Czech [PBS TJ100](https://en.wikipedia.org/wiki/PBS_Velka_Bites_TJ100).
* Western electronics (Texas Instruments, Analog Devices) continue to be
  identified — same supply chain as Shahed-136.
* The Russian-fielded equivalent is the **Geran-3** (see
  [`geran-3.md`](geran-3.md)), with the Telefly JT80 turbojet substituted
  for the Tolou-10.

## Family relationship

```
HESA Shahed-136 (piston, IR)
  ├─ Geran-2 (RU-licensed copy)
  ├─ Shahed-238 (jet variant, IR)
  │     └─ Geran-3 (RU-licensed copy with Chinese Telefly JT80)
  ├─ Shahed-131 (smaller decoy/strike)
  │     └─ Geran-1 (RU-licensed)
  └─ Geran-4 (RU-built turbojet, mesh-networked)
```
