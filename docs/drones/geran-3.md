# Geran-3 (Series U — turbojet variant)

> Russian-produced jet-powered loitering munition, modeled on the Iranian
> Shahed-238. The Geran-3 dramatically reduces Ukrainian air-defense reaction
> time by raising cruise speed to **550–650 km/h**.

| | |
|---|---|
| **Slug** | `uav-geran-3` |
| **Operators** | 🇷🇺 RU |
| **Role** | Loitering munition (high-speed long-range strike) |
| **Propulsion** | 🇨🇳 Telefly **JT80** turbojet (~50 kgf thrust) — Iranian *Tolou-10/13* is an unlicensed copy of the Czech [PBS TJ100](https://en.wikipedia.org/wiki/PBS_Velka_Bites_TJ100) |
| **Cruise speed** | 250–300 km/h (loiter), ~550–650 km/h (terminal) |
| **Primary source** | <https://war-sanctions.gur.gov.ua/en/page-geran-3> |

## Documented components (from GUR teardown, Series U)

| # | Component | Marking | Manufacturer | Country |
|---|---|---|---|---|
| 1 | Turbojet engine | Telefly **JT80** | Telefly Telecommunications | 🇨🇳 CN |
| 2 | Fuel pump | Bosch 0 580 254 044 111-30 | Bosch | 🇩🇪 DE |
| 3 | Brushless motor | X2820-5 KV:1100 | SunnySky | 🇨🇳 CN |
| 4 | Digital servo drive | SERV 01.02-150-15-PWM V2 | GXSERVO | 🇨🇳 CN |
| 5 | N-channel MOSFET | AON6324 6324 GVOY1X | Alpha & Omega Semiconductor | 🇺🇸 US |
| 6 | Motor driver | EG2134 CSFA01 HTFA09 | EGmicro / Yijing Microelectronics | 🇨🇳 CN |
| 7 | Memory chip | 24M02RD K328K | STMicroelectronics | 🇨🇭 CH |
| 8 | 32-bit MCU | **STM32F070CBT6** | STMicroelectronics | 🇨🇭 CH |
| 9 | 32-bit MCU | **STM32F103C8T6** | STMicroelectronics | 🇨🇭 CH |
| 10 | RS-232 transceiver | 3232EE 2337L K0379 | Sipex Corp. | 🇺🇸 US |
| 11 | Multi-channel RS-232 driver/receiver | MB3238I 52K G4 C05X | Texas Instruments | 🇺🇸 US |
| 12 | Power connector | AMASS | AMASS | 🇨🇳 CN |
| 13 | GNSS receiver | (proprietary) | Not identified | UNK |
| 14 | INS | SADRA | (Iranian-origin) | 🇮🇷 IR |
| 15 | Anti-jam GNSS | "Comet" (Russian domestic) | VNIIR-PROGRESS JSC | 🇷🇺 RU |
| 16 | Wilkinson splitter | 2-Way 800-2700 MHz | (specialty RF) | UNK |
| 17 | ADC | AIRDATA COMPUTER | Not identified | UNK |

Sources: GUR War & Sanctions Portal, [BusinessInsider analysis](https://www.businessinsider.com/russia-jet-powered-drone-immune-electronic-warfare-ukraine-says-2025-9), [Militarnyi.com](https://militarnyi.com/en/news/russians-demonstrate-jet-version-of-shahed-kamikaze-drone/).

## Why Geran-3 matters

1. **Speed shift** breaks the IADS engagement timeline that worked against Geran-2.
2. **STM32F1/F0 + Bosch fuel pump** are commercial parts widely available on AliExpress — illustrating the **white-goods diversion** problem documented by [CEPA](https://cepa.org/article/western-chips-power-russias-war/).
3. The **Tolou-10 / JT80** turbojet is described as an unlicensed copy of the Czech [PBS TJ100](https://militarnyi.com/en/news/russians-demonstrate-jet-version-of-shahed-kamikaze-drone/) — extending Iranian/Russian dependence on commercial engine IP.
