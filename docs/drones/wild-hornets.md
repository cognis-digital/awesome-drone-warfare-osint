# Wild Hornets ("Дикі шершні")

> Ukrainian **non-profit charity** — not a company — producing combat
> drones for the Armed Forces of Ukraine. Funded entirely by private
> donations. Built around 3D-printed airframes. Operates with **~25
> engineers producing 100 drones/day**, **65 % locally sourced parts**.

| | |
|---|---|
| **Founded** | Spring 2023 |
| **Engineers** | ~25 |
| **Production** | 100 drones/day |
| **Local sourcing** | 65 % |
| **Notable products** | **Sting** interceptor, **Queen Hornet** bomber, **Wild Dragon** (thermite), standard Wild Hornet FPV |
| **Sources** | [Official site](https://wildhornets.com/en/) · [Wikipedia](https://en.wikipedia.org/wiki/Wild_Hornets) · [Reuters](https://www.reuters.com/business/aerospace-defense/inside-ukrainian-interceptor-drones-wanted-around-gulf-2026-03-17/) · [Ukrainian Arms Monitor](https://ukrainesarmsmonitor.substack.com/p/sting-interceptor-drone-by-wild-hornets) |

## Sting interceptor (anti-Shahed FPV)

| Spec | Value |
|---|---|
| Frame | 3D-printed (PLA / PETG hybrid) |
| Top speed | **100 mph (160 km/h)** |
| Cruise altitude | 10,000 ft (3,000 m) |
| Cost | **$1,000 – $5,000** depending on optics/payload |
| Thermal optics | Odd Systems "Kurbas" |
| **Confirmed Shahed kills (per March 6, 2026)** | **3,900+** |

The Sting is mission-critical: a Shahed-class drone Russia produces for
~$20–80k is regularly killed by a Sting costing 4-200× less. This is the
counter-economics that made the [Reuters interceptor exposé](https://www.reuters.com/business/aerospace-defense/inside-ukrainian-interceptor-drones-wanted-around-gulf-2026-03-17/)
viral with Gulf-state customers.

## Other Wild Hornets products

| Drone | Type | Notes |
|---|---|---|
| **Queen Hornet** | 17-inch FPV bomber | 9 kg payload, 20 km range |
| **Wild Dragon** | Thermite payload | Co-developed with Steel Hornets |
| Standard Wild Hornet | Kamikaze FPV | 3-6 lb payload, 100 mph |

## Components observed (open-source consensus)

- **Flight controller**: Pixhawk Cube Orange / Speedybee variants
- **Companion computer**: Raspberry Pi Zero 2 (for some autonomy modes)
- **Video TX**: DJI O3, Walksnail, custom encrypted analog
- **GPS**: u-blox, Holybro variants
- **Battery**: Tattu, GNB, locally repackaged

See [`docs/playbooks/electronic-warfare.md`](../playbooks/electronic-warfare.md) for the broader EW context.
