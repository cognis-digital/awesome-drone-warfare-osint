# What worked, what didn't — drone warfare by the numbers (2022–2026)

> **Analytical, defensive, descriptive.** This page collects *publicly reported*
> figures on drone effectiveness, countermeasures, and the foreign-component
> supply chain. It contains no operational, assembly, or targeting guidance.
> Belligerent self-reported claims (e.g. by GUR or either defense ministry) are
> labelled and should be cross-checked against the primary sources linked.
> Figures were compiled from the cited reporting; **verify against the primary
> pages before citing.** See [DISCLAIMER.md](../DISCLAIMER.md).

## 1. Drones now dominate the battlefield

| Claim | Figure | Source |
|---|---|---|
| Share of battlefield casualties attributed to drones | ~70–80% | [Army Technology](https://www.army-technology.com/news/drones-now-account-for-80-of-casualties-in-ukraine-russia-war/) |
| Ukrainian-stated share of battlefield hits that are drone-delivered | >80% | [Zelenskyy via Yahoo](https://www.yahoo.com/news/articles/over-80-every-battlefield-hit-073425388.html) |
| Russian personnel struck by FPV drones, Dec 2024 (Ukraine USF claim) | 33,019 — first month drones out-paced Russian recruitment | [Kyiv Post](https://www.kyivpost.com/post/67606) |
| Targets Ukraine claims struck by drones across 2025 | ~820,000 | [Kyiv Post](https://www.kyivpost.com/post/67606) |

## 2. Loitering-munition saturation — mass beats hit-rate

| Claim | Figure | Source |
|---|---|---|
| Shahed/Geran launch rate, pre-Sep 2024 → Mar 2025 | ~200/week → >1,000/week | [CSIS](https://www.csis.org/analysis/drone-saturation-russias-shahed-campaign) |
| Shahed share intercepted/failed to reach target | ~90% | [CSIS](https://www.csis.org/analysis/calculating-cost-effectiveness-russias-drone-strikes) |
| Effective cost per Shahed *target struck* (despite ~90% loss) | ~$350k (vs ~$1M for a Kh-22) at ~$35k/unit | [CSIS](https://www.csis.org/analysis/calculating-cost-effectiveness-russias-drone-strikes) |
| One-way attack drones launched Sep 2022–Dec 2024 | >14,700 (of >19,000 total missiles+OWA) | [CSIS](https://www.csis.org/analysis/calculating-cost-effectiveness-russias-drone-strikes) |

**What this shows:** the loitering-munition model trades a low per-shot hit rate
for cost asymmetry and magazine depth — defenders win most engagements yet still
lose on cost-per-intercept.

## 3. Electronic warfare — the most effective counter, and its limits

| Claim | Figure | Source |
|---|---|---|
| Accuracy of GPS-guided JDAM-ER / Excalibur under Russian jamming | fell from ~70% to low single digits (Excalibur <10%, withdrawn) | [Washington Post](https://www.washingtonpost.com/world/2024/05/24/russia-jamming-us-weapons-ukraine/) |
| US response: anti-jam (Home-on-Jam) investment | $75M reallocated; $23.5M contract for JDAM-ER HOJ | [Forensic Archive](https://medium.com/@Forensic-Archive/pentagon-spent-75m-on-anti-jamming-kits-after-ukraines-hack-but-did-it-work-f12c58ca2dd2) |
| Fiber-optic FPV (immune to RF jamming) — Ukrainian makers by early 2026 | 35+ manufacturers; Russian frontline adoption 30–50% in some units | [Defense Advancement](https://www.defenseadvancement.com/feature/evolving-countermeasures-for-the-rise-of-fiber-controlled-drones/), [JED](https://www.jedonline.com/2025/05/15/nato-seeks-solutions-for-fiber-optic-fpv-drones/) |

**What this shows:** GNSS denial is the single most effective counter to
precision/GNSS-reliant munitions — which is *why* fiber-optic-tethered and
GNSS-omitting short-range FPVs emerged to route around it. Countermeasure and
counter-countermeasure co-evolve.

## 4. Counter-UAS — layers beat single systems

| Approach | Reported performance | Source |
|---|---|---|
| Layered C-UAS (detect + EW + kinetic), aggregate | 85–93% interception | [Euro S&D](https://euro-sd.com/2025/09/articles/exclusive/46573/countering-small-drones-a-big-challenge/) |
| High-power microwave (Epirus Leonidas), live-fire | 61/61 drones; defeated a 49-drone swarm (100%) | [Epirus](https://www.epirusinc.com/press-releases/epirus-leonidas-high-power-microwave-defeats-49-drone-swarm-100-of-drones-flown-at-live-fire-demonstration) |
| Kinetic interceptor (Raytheon Coyote) program | ~$5.04B Army ordering vehicle (Coyote + KuRFS radar) | [Army Recognition](https://www.armyrecognition.com/news/army-news/2025/pentagon-awards-raytheon-5-04b-army-contract-for-coyote-counter-uas-and-kurfs-radars) |
| Drone-on-drone interceptors vs Lancet (Ukraine claim) | up to ~90% reduction in successful strikes | [Drone Warfare](https://drone-warfare.com/counter-uas/drone-defeat/) |
| C-UAS market size | $5.99B (2024) → $20.31B (2030), 25.1% CAGR | [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/counter-cuas-systems-market-4197284.html) |

## 5. The foreign-component / sanctions-evasion story

| Claim | Figure | Source |
|---|---|---|
| GUR "War & Sanctions" portal scope (early 2026) | 5,626 components / 195 weapon types; 2,805 in 79 UAV types | [GUR](https://war-sanctions.gur.gov.ua/en/page-shahed-136) |
| US-origin share of parts in Shahed/Geran family (GUR) | ~60% | [Türkiye Today](https://www.turkiyetoday.com/world/60-of-russian-iranian-drone-parts-are-us-made-says-ukrainian-intelligence-3218207) |
| CAR teardown of Iranian Shahed/Mohajer | 500+ distinct components, "almost exclusively" Western/Asian | [Business & Human Rights Centre](https://www.business-humanrights.org/en/latest-news/russia-two-thirds-of-foreign-components-in-drones-used-in-attacks-on-ukraine-originate-from-us-new-research-shows-revealing-gaps-in-sanctions-regime/) |
| AI compute in a loitering munition | upgraded Shahed-136 with camera + NVIDIA Jetson Orin (GUR) | [GUR](https://gur.gov.ua/en/content/warsanctions-rozkryvaie-nachynku-modernizovanoho-shahed136-vyrobnytstva-iranu-z-kameroiu-ta-shtuchnym-intelektom) |
| EU components routed via Hong Kong shells (first 2 post-invasion yrs) | >€190M | [Follow the Money](https://www.ftm.eu/articles/russia-war-ukraine-european-tech-hidden-supply-chain) |
| US oversight corroboration | US Senate HSGAC majority staff report, Sep 10 2024 | [HSGAC (PDF)](https://www.hsgac.senate.gov/wp-content/uploads/09.10.2024-Majority-Staff-Report-The-U.S.-Technology-Fueling-Russias-War-in-Ukraine.pdf) |

This is the thread this dataset documents at the component level: the
[`data/components.csv`](../data/components.csv) (8,300+ rows), [`teardowns`](../data/teardowns.csv),
and [`supply_chain_edges`](../data/supply_chain_edges.csv) tables map *which*
foreign parts appear in *which* platforms, per the primary teardown sources.

---

*Cross-references: [counter-UAS playbook](playbooks/counter-uas.md) ·
[electronic-warfare playbook](playbooks/electronic-warfare.md) ·
[supply-chain playbook](playbooks/supply-chain.md) ·
[autonomy & AI playbook](playbooks/autonomy-ai.md) · [sources](sources.md).*
