# Geran-4 (turbojet variant)

> The most recently observed variant of the Russian-built Shahed/Geran family.
> Notable for switching from a piston engine to a Chinese-produced turbojet.

| | |
|---|---|
| **Slug** | `geran-4-uav` |
| **Operators** | 🇷🇺 RU |
| **Role** | Loitering munition (long-range strike) |
| **Propulsion** | 🇨🇳 Telefly LX-WP-160 turbojet |
| **Documented foreign components (so far)** | _live count — see `data/components.csv`_ |
| **Primary source** | <https://war-sanctions.gur.gov.ua/en/components> (filter Armament = "Geran-4 UAV") |

## Notable components

These are sampled directly from the GUR portal:

| Marking | Manufacturer | Country | Function |
|---|---|---|---|
| LX-WP-160 turbojet | Telefly Telecommunications Equipment Co. | 🇨🇳 CN | Propulsion |
| (servo drive) | Not identified | UNK | Control surface actuation |
| (solid-state DC relay) | FOTEK Controls | 🇹🇼 TW | Power switching |
| Network switch | SCYTON Technology | 🇨🇳 CN | Datalink |
| Mesh modem "Tech Mesh Network XK" | Xingkay Tech | 🇨🇳 CN | C2 |
| Connector 21 12 LA J30JZLN21ZKWA | Nanjing Kaida Optoelectronics | 🇨🇳 CN | Interconnect |
| Transceiver MAX3232 EUE | Maxim / Analog Devices | 🇺🇸 US | RS-232 |
| Memory chip 5KA17 RW214 | Micron Technology | 🇺🇸 US | Flash |
| Transceiver 55ASLHK G4 LVC16T245 | Texas Instruments | 🇺🇸 US | Logic |
| Transceiver SIT3232E DH2479 | Hunan Silicon IoT Tech | 🇨🇳 CN | RS-232 |

## Why Geran-4 matters

The shift from piston (Geran-2) → turbojet (Geran-4) substantially increases
cruise speed, complicating air-defense intercept timing. The fact that the
turbojet is a **Chinese commercial product** (Telefly LX-WP-160) — together
with the integration of Chinese mesh-modem and Chinese network-switch
hardware — confirms a deepening Russia↔China components pipeline.

Cross-reference: [CSIS — China's UAV Supply Chain Restrictions](https://www.csis.org/analysis/why-chinas-uav-supply-chain-restrictions-weaken-ukraines-negotiating-power)
