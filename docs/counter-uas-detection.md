# Counter-UAS: detection & identification (defensive reference)

> **Analytical, defensive, descriptive.** How hostile drones are *detected,
> classified, and identified* for situational awareness, plus the publicly
> documented defensive-effector landscape and the governing standards. No
> drone-control, flight-command, targeting, or defeat-procedure content. Figures
> are publicly reported; **verify against the linked primary sources** (CSIS, FAA,
> NDSS, RUSI PDFs) before citing. See [DISCLAIMER.md](../DISCLAIMER.md).

## Threat framing — sUAS groups

US DoD groups uncrewed aircraft 1–5; counter-UAS focuses on **small UAS (Groups 1–3)**:
Group 1 (≤20 lb, <1,200 ft AGL, <100 kt), Group 2 (≤55 lb, <3,500 ft, <250 kt),
Group 3 (<1,320 lb, <18,000 ft, <250 kt). The threat profile — cheap, proliferated,
low-signature, multi-mission — is why layered defense is the consensus.
Sources: [CSIS, *Countering Small UAS* (2023, PDF)](https://csis-website-prod.s3.amazonaws.com/s3fs-public/2023-11/231114_Shaikh_Countering_sUAS.pdf) ·
[CRS IF12797](https://www.congress.gov/crs-product/IF12797).
A core policy distinction: **detection** (detect/track/identify) is legally separate
from **mitigation** (disabling/taking control), which is tightly restricted —
[CISA, *Be Air Aware*](https://www.cisa.gov/topics/physical-security/be-air-aware/protect-critical-infrastructure-and-public-gatherings).

## Detection modalities (no single sensor suffices → sensor fusion)

| Modality | How it detects | Publicly reported reach / notes | Key limitation |
|---|---|---|---|
| **RF / spectrum** (passive) | Direction-finds the drone↔controller link; matches FHSS signatures (433/900 MHz, 2.4/5.8 GHz) | High classification accuracy (protocol match) | Blind to **autonomous/fiber-optic** drones (no RF link) |
| **Radar** (micro-Doppler) | Physics-based; rotor blades give a Doppler modulation distinct from birds | Echodyne EchoShield ~1.5 km (tiny UAS) → ~7.9 km (small fixed-wing), 25 km instrumented; Robin IRIS classifies ~3 kg drone to ~2 km | Small RCS in urban/ground clutter |
| **Acoustic** (passive) | Motor/propeller signature via mic arrays | ~300–500 m typical; research arrays reliable ~70–100 m | Wind/noise/temperature degrade range |
| **EO / IR** | Visual/thermal confirmation + forensic record | Usually radar/RF-cued, not wide-area search | Lighting/weather/obscurants; narrow FoV |

Sources: [EU JRC C-UAS tech (PDF)](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC140692/JRC140692_01.pdf) ·
[Robin Radar micro-Doppler](https://www.robinradar.com/blog/how-micro-doppler-radar-works) ·
[Echodyne EchoShield](https://www.echodyne.com/radar-systems/echoshield) ·
[Robin Radar acoustic](https://www.robinradar.com/blog/acoustic-sensors-drone-detection) ·
[PMC, RF identification signals](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10490811/) ·
[US Army, fiber-optic drones C-UAS challenge](https://www.army.mil/article/287737/fiber_optic_drones_posing_a_significant_c_uas_challenge).

## Identification & classification

- **Track → "is it a drone?"** Radar pairs micro-Doppler features with neural nets;
  RF/acoustic ML pipelines report accuracy that scales down with class count (e.g. RF
  DNN ~99.7% for 2 types, ~46.8% for 10).
  [Frontiers, ML for drone detection](https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2024.1440727/full) ·
  [arXiv RF-fingerprint residual nets](https://arxiv.org/pdf/2011.13663).
- **Protocol/type ID — DJI DroneID/OcuSync.** Reverse-engineered (NDSS 2023); DroneID is
  broadcast **unencrypted**, carrying drone + operator location, so an SDR receiver can
  passively identify/locate DJI drones (open analogue to the commercial AeroScope).
  [NDSS 2023 paper (PDF)](https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f217_paper.pdf) ·
  [RUB-SysSec DroneSecurity](https://github.com/RUB-SysSec/DroneSecurity).
- **RF fingerprinting** of FHSS control links (ELRS/Crossfire): hopping patterns +
  transmitter hardware imperfections → type attribution.
  [arXiv, RF fingerprints w/ interference](https://arxiv.org/pdf/1909.05429).

## C-UAS effectors landscape (defender's view — descriptive only)

Categories and publicly reported outcomes — **no operating/engagement procedures**:
- **EW / link disruption ("soft kill")** — most common non-kinetic layer; *ineffective
  against fiber-optic/autonomous drones* (no link). [RUSI, *Protecting the Force*](https://www.rusi.org/explore-our-research/publications/occasional-papers/protecting-force-uncrewed-aerial-systems).
- **Directed energy / HPM** — area effect, counter-swarm, cheap per shot. AFRL **THOR**
  swarm demo (Apr 2023); **Epirus Leonidas** publicly reported first HPM defeat of a
  **fiber-optic** drone (Jan 2026) — notable since fiber drones are EW-immune.
  [AFRL THOR](https://www.afrl.af.mil/News/Article-Display/Article/3396995/afrl-conducts-swarm-technology-demonstration/) ·
  [Epirus](https://www.epirusinc.com/press-releases/epirus-leonidas-demonstrates-successful-use-of-high-power-microwave-to-defeat-fiber-optic-controlled-uas).
- **High-energy laser** — one target at a time; **kinetic interceptors / nets** — hard-kill/
  capture layer. Layered defense beats any single effector. [CSIS PDF](https://csis-website-prod.s3.amazonaws.com/s3fs-public/2023-11/231114_Shaikh_Countering_sUAS.pdf).

## Standards, frameworks & policy

- **FAA Remote ID (14 CFR Part 89)** — drones broadcast identity + location ("digital
  license plate"); operator deadline 16 Sep 2023, enforcement discretion to 16 Mar 2024.
  [FAA Final Rule (PDF)](https://www.faa.gov/sites/faa.gov/files/2021-08/RemoteID_Final_Rule.pdf).
- **ASTM F3411** — Remote ID message formats (Broadcast + Network). **Caveat:** F3411-22a
  does **not** mandate authentication, so Remote ID can be spoofed — it's an ID *aid*, not
  trusted authentication. [ASTM](https://store.astm.org/f3411-22a.html) ·
  [arXiv TBRD](https://arxiv.org/pdf/2510.11343).
- **DHS/CISA** detection guidance (detection ≠ mitigation; legal review before
  intercepting comms); **CRS R48477** (DoD C-UAS); **Army ATP 3-01.81**; **NIST** aerial
  test methods. [CISA](https://www.cisa.gov/topics/physical-security/be-air-aware/protect-critical-infrastructure-and-public-gatherings) ·
  [CRS R48477](https://www.congress.gov/crs-product/R48477) ·
  [ATP 3-01.81 (PDF)](https://irp.fas.org/doddir/army/atp3-01-81.pdf) ·
  [NIST](https://www.nist.gov/news-events/news/2018/12/nist-performance-tests-aerial-response-robots-become-national-standard).

---
*Companion to the [counter-UAS playbook](playbooks/counter-uas.md),
[electronic-warfare playbook](playbooks/electronic-warfare.md), and
[STATISTICS.md](STATISTICS.md). Full source list inline above.*
