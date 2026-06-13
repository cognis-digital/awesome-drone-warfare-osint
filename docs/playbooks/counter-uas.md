# Counter-UAS taxonomy

> A layered C-UAS stack typically combines **detection**, **tracking**,
> **identification**, **decision**, and **mitigation** in a sensor-shooter
> loop. This page indexes the open literature.

## Detection layers

| Layer | Sensor | Range | Notes |
|---|---|---|---|
| **RF detection** | Spectrum sniffer (DroneShield, Aaronia, CRFS) | up to 25 km | Detects controllers + downlinks |
| **Radar** | X / Ku / S-band (Robin Radar IRIS, RPS-42, Echodyne) | 1-15 km | Limited vs. small RCS |
| **Acoustic** | Mic arrays (Boson, Squarehead) | 100-500 m | Last-mile, terrain-limited |
| **EO/IR** | Boson, Tau-2, custom NUC (Spynel, FLIR) | 1-5 km | Visual confirmation |
| **Cyber** | Protocol-aware fingerprinting | (post-detect) | DJI / ELRS / Crossfire identification |

## Mitigation layers

| Mitigation | System | Cost / shot | Notes |
|---|---|---|---|
| **RF jamming** | DroneGun, Anduril Anvil-X, Bukovel-AD | $0 (electric power) | Defeats COTS C2/GPS; ineffective vs. fiber |
| **GPS spoof** | Ukraine Pokrova | $0 | Mass deception |
| **Kinetic — gun** | Smartshooter Smash 3000 (rifle sight) | <$5 | Skilled shooter only |
| **Kinetic — SAM** | Pantsir, Coyote Block 3, RIM-116 RAM | $100k–$3M | Overkill vs. Shahed; magazine depletion |
| **Kinetic — drone-on-drone** | **Wild Hornets Sting**, Anduril Bolt | $1-10k | Cost-favorable; **3,900+ Shahed kills** |
| **Directed energy** | UK DragonFire, US HELWS, IL Iron Beam | $1-10 / shot | Maturing; weather-limited |
| **Microwave** | EpiRus Leonidas, Phaser | $0/sweep | Swarm defeat; range-limited |
| **Nets / drones** | Ukrainian "Bumblebee" net-droppers | $0 | Slow, opportunistic |

## Vendor + doctrine landscape

- **JIATF-401** (US Army) — Anduril Lattice as enterprise C2 ([Anduril](https://www.anduril.com/news/jiatf-401-selects-lattice-as-enterprise-tactical-command-and-control-platform-for-c-uas))
- **C-UAS Hub** — vendor index ([cuashub.com](https://cuashub.com/))
- **DroneSec OSINT** — counter-drone threat-intel feed ([dronesec.com](https://dronesec.com/))
- **NATO EUFOR/MMC** — multi-national C-UAS doctrine
- **Pentagon CRRUAS** — Counter-Rocket / Artillery / Mortar / Drone

## The "magazine economics" problem

Engaging $30k Shahed-136s with $3M Standard SM-2 missiles is unsustainable.
The current direction across all Western forces is:
1. Push to **$10-100/shot** layers (directed energy, drone-on-drone, gun);
2. **Layer cheap kill chains in front** of expensive SAMs;
3. Increase **detection range** so cheaper effectors get the shot.

This is the doctrinal homework documented in [Ifri's eight lessons](https://www.ifri.org/en/studies/mapping-miltech-war-eight-lessons-ukraines-battlefield)
and the [Hudson rise/fall of EW](https://www.hudson.org/national-security-defense/the-fall-and-rise-of-russian-electronic-warfare).
