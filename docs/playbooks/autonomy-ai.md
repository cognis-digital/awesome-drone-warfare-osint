# Autonomy and AI in modern drone warfare

> An honest read of where AI/ML is — and isn't — on the 2025-2026 battlefield.

## Where AI is real today

| Capability | Where it's used | Evidence |
|---|---|---|
| **Terminal target lock** (last-mile visual tracking) | Bumblebee, Liutyi (CNN), Lancet-3 (Jetson) | [NYT](https://www.nytimes.com/2025/12/31/magazine/ukraine-ai-drones-war-russia.html), [ISIS-online](https://isis-online.org/isis-reports/russian-lancet-3-kamikaze-drone-filled-with-foreign-parts) |
| **Link-loss flight** | Spider's Web FPVs | [CSIS](https://www.csis.org/analysis/how-ukraines-spider-web-operation-redefines-asymmetric-warfare), [Wikipedia](https://en.wikipedia.org/wiki/Operation_Spiderweb) |
| **Visual navigation against jammed GPS** | AQ-400 Scythe (laser altimeter + visual), ArduPilot dead-reckoning | Wikipedia, ArduPilot docs |
| **Sensor-fusion C2** | Anduril Lattice, Auterion OS | Vendor docs |
| **Swarming (leader-follower)** | AQ-400 Scythe, Swarmer (UA) | Wikipedia, [Ukrainian Arms Monitor](https://ukrainesarmsmonitor.substack.com/p/drone-warfare-in-ukraine-the-interplay) |

## Where AI is NOT yet operational (as of June 2025)

> "**Promises of an immediate AI/ML drone revolution are premature as of
>  June 2025**, given that both Russian and Ukrainian forces will need to
>  resolve significant data, infrastructure, and tactical challenges
>  before AI is decisive."
> — [ISW battlefield AI assessment](https://understandingwar.org/research/russia-ukraine/the-battlefield-ai-revolution-is-not-here-yet-the-status-of-current-russian-and-ukrainian-ai-drone-efforts/)

The bottleneck is **training data + compute on-airframe + comms**, not
algorithms. A Jetson Orin Nano can run YOLO-class detection at ≥20 FPS
but battery, optics, and the **ground-truth label problem** still rule.

## Hardware in the AI kill chain

| Module | Use case |
|---|---|
| **NVIDIA Jetson TX2** | Lancet-3 (per ISIS) |
| **NVIDIA Jetson Orin Nano / NX** | Newer UA + RU FPVs |
| **Raspberry Pi 4/5/Zero 2** | Ukrainian NORDA Dynamics autonomy stack ([Ukrainian Arms Monitor](https://ukrainesarmsmonitor.substack.com/p/towards-greater-drone-autonomy-norda)) |
| **STM32H7 / ESP32** | Lightweight inference on flight controller |
| **Auterion Skynode S** | Edge inference + Pixhawk-class FC ([Auterion](https://auterion.com/product/skynode-s/)) |

## Software stacks in public deployment

- **ArduPilot** ([github](https://github.com/ArduPilot/ardupilot)) — used in Spider's Web
- **PX4** ([github](https://github.com/PX4/PX4-Autopilot)) — Auterion-hardened in Skynode
- **AuterionOS** — commercial PX4 fork ([docs](https://docs.px4.io/main/en/companion_computer/auterion_skynode))
- **Betaflight / iNav / Cleanflight** — FPV
- **NORDA Dynamics** — Ukrainian autonomy stack tuned for Raspberry Pi

## Policy / doctrine

- US **Project Maven** — AI for target ID, now in active strike ops ([Wikipedia](https://en.wikipedia.org/wiki/Project_Maven), [Al-Monitor](https://www.al-monitor.com/originals/2026/04/ai-war-five-things-know-about-project-maven))
- US **Project Linchpin** — Army's first AI program-of-record ([Defenscoop](https://defensescoop.com/2023/05/10/project-linchpin-aims-to-set-army-on-sustainable-path-toward-integrating-ai-into-weapons-programs/))
- Ukraine — **Brave1 cluster** ([brave1.gov.ua](https://brave1.gov.ua/en/)) brings together AI startups and the MoD
- China — building a [sovereign drone-AI ecosystem](https://www.csis.org/analysis/how-russia-building-sovereign-drone-ecosystem-ai-driven-autonomy)
