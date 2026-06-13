# Lancet family (ZALA Aero)

> Russian-produced loitering munition, manufactured by ZALA Aero Group
> (part of Kalashnikov Concern). Used extensively against Ukrainian
> artillery, air-defense, and armored vehicles. Forensics show
> heavy reliance on Western AI accelerators and electric motors.

| | |
|---|---|
| **Models** | Lancet-1, Lancet-3, **Izdeliye-51** (larger), **Izdeliye-52**, **Izdeliye-53** (4-tube launcher), Lancet-E (export) |
| **Operators** | 🇷🇺 RU |
| **Role** | Tactical loitering munition |
| **Propulsion** | Electric (brushless, externally sourced) |
| **Primary sources** | [ISIS-online Lancet-3 report](https://isis-online.org/isis-reports/russian-lancet-3-kamikaze-drone-filled-with-foreign-parts) · GUR portal entry [Izdeliye-51 (Lancet)](https://war-sanctions.gur.gov.ua/en/uav/365) |

## Specifications (Izdeliye-51)

| Spec | Value |
|---|---|
| Warhead | 5 kg |
| Flight time | 40 min |
| Speed | 80 km/h cruise (≈110 km/h max, 300 km/h dive) |
| Communication distance | 50 km |
| Propulsion | Electric |

## Critical Western components (ISIS-online forensics)

| Component | Manufacturer | Country | Function |
|---|---|---|---|
| **Jetson TX2** AI module | **NVIDIA** | 🇺🇸 US | On-board image processing + autonomous target ID |
| **u-blox** GNSS module | u-blox | 🇨🇭 CH | GPS / Galileo / GLONASS / BeiDou — has anti-jam & anti-spoof |
| **AXI 5330 Gold Line** brushless motor | AXI Model Motors | 🇨🇿 CZ | Propulsion |
| Multiple TI / ADI ICs | TI, ADI | 🇺🇸 US | Telemetry & control |

> **The NVIDIA Jetson finding** is significant: it places a US AI accelerator
> directly in the kill chain of an autonomous loitering munition. See the
> [ISIS-online report](https://isis-online.org/isis-reports/russian-lancet-3-kamikaze-drone-filled-with-foreign-parts).

## Larger Izdeliye family

- **Izdeliye-51** — larger than Lancet-3; uses pneumatic launcher.
- **Izdeliye-52** — direct evolution of Lancet-3.
- **Izdeliye-53** — fired from a **4-tube pneumatic launcher**; enables
  saturation-fire tactics. ([ISIS](https://isis-online.org/isis-reports/russian-lancet-3-kamikaze-drone-filled-with-foreign-parts))

Cross-reference [`autonomous-weaponswatch entry`](https://autonomousweaponswatch.org/weapon/kalashnikov-zala-lancet-3) for export marketing claims.
