# Operation Spider's Web (1 June 2025)

> The single most consequential drone operation of the war. The SBU
> destroyed approximately **one-third of Russia's strategic bomber
> fleet** using **117 truck-launched FPV drones** running open-source
> ArduPilot.

| | |
|---|---|
| **Date** | 1 June 2025 |
| **Executing agency** | Security Service of Ukraine (SBU) |
| **Drones used** | 117 × "Osa" (Wasp) quadcopter FPVs (~3.2 kg payload each) |
| **Flight stack** | **ArduPilot** with dead-reckoning + AI link-loss compensation |
| **Targets (5 airbases)** | Belaya · Dyagilevo · Ivanovo Severny · Olenya · Ukrainka |
| **Aircraft destroyed/damaged** | Tu-95MS, Tu-22M3, Tu-160 strategic bombers + A-50 AEW&C |
| **Sources** | [Wikipedia](https://en.wikipedia.org/wiki/Operation_Spiderweb) · [CSIS](https://www.csis.org/analysis/how-ukraines-spider-web-operation-redefines-asymmetric-warfare) · [Janes](https://www.janes.com/defence-intelligence-insights/defence-and-national-security-analysis/operation-spiderweb-ukraine-covert-drone-strike-inside-russia) · [Chatham House](https://www.chathamhouse.org/2025/06/ukraines-operation-spiders-web-game-changer-modern-drone-warfare-nato-should-pay-attention) |

## Technical novelty

1. **Dead-reckoning autopilot**: ArduPilot can fly inertial+pre-mapped
   waypoints when GNSS is jammed. The Spider's Web drones used this
   mode to navigate inside Russian EW bubbles.
2. **AI link-loss handling**: onboard ML guided drones during the
   brief windows when the SBU operator was disconnected.
3. **Truck launch**: drones were smuggled in disassembled containers
   to clandestine sites near each airbase, then launched in unison.
4. **Strategic-aviation kill**: Russia subsequently dispersed remaining
   bombers to remote bases (Olenya → Anadyr / Engels), shrinking sortie
   tempo.

## Why this matters for the dataset

- The flight stack is **open-source upstream** ([ArduPilot](https://github.com/ArduPilot/ardupilot)) — anyone can audit the same code.
- The kinetic effect from **~$1,000 drones** destroying **$50M bombers** is the canonical demonstration of the [cost-asymmetry math](https://cepa.org/article/ukraine-attack-the-spiders-web-still-needs-humans/) that drives 21st-century drone warfare.
- Janes and Chatham House both argue NATO has **no comparable doctrine**: a wake-up call documented across the [`docs/playbooks/`](../playbooks/index.md) section.
