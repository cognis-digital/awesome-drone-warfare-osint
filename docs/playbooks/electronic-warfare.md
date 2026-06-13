# Electronic warfare playbook (defensive / academic)

> **Scope:** descriptive doctrine and open literature only. This page does
> **not** host RF code, IQ recordings, or jammer schematics. See
> [`DISCLAIMER.md`](../../DISCLAIMER.md).

## Threat surfaces

| Subsystem | Jamming surface | Open countermeasure literature |
|---|---|---|
| GNSS (GPS L1/L2, GLONASS, Galileo, BeiDou) | Wideband noise & spoofing | CRPA antennas, INS-only fallback (e.g. GUR SADRA), Septentrio anti-spoof, u-blox SecureNAV |
| C2 (915 MHz, 2.4 GHz, 5.8 GHz) | Spot, sweep, barrage jamming | Frequency-hopping, mesh networking (Geran-4) |
| Video downlink (analog 5.8 GHz, DJI O3/O4 digital) | Same-band saturation | Encrypted digital links, **fiber-tether** (last-mile FPV) |
| Data telemetry | C2-class | LoRa fallback, satellite relay |
| Inertial navigation | (not jammable) | Dead-reckoning + visual odometry (Spider's Web) |

## GPS jamming & spoofing — documented incidents

* **Kaliningrad-origin jamming** has driven Ukrainian drones into NATO airspace ([United24](https://united24media.com/war-in-ukraine/russian-jamming-from-kaliningrad-is-sending-ukrainian-drones-toward-nato-states-telegraph-reports-19142)).
* **Lithuania has warned** of Russian capability to falsify GPS signals deep into Europe ([Reddit/worldnews](https://www.reddit.com/r/worldnews/comments/1to6wtd/russia_can_falsify_gps_signals_deep_into_europe/)).
* **Ukraine's Pokrova** system spoofs GPS countrywide vs. Russian drones ([RNTF](https://rntfnd.org/2024/02/03/ukraine-will-spoof-gps-across-the-country-to-stop-russian-drones-new-scientist/)).

## Fiber-optic FPV — the EW counter-counter

Both sides now deploy **5-50 km fiber-tethered FPVs** that are **immune to RF jamming** ([Wikipedia](https://en.wikipedia.org/wiki/Fiber_optic_drone), [Atlantic Council](https://www.atlanticcouncil.org/blogs/ukrainealert/fiber-optics-drones-have-emerged-as-critical-kit-for-both-russia-and-ukraine/)). Side effects:
- Russian fiber-optic drones contributed to Ukrainian vehicle losses up
  by **25 %** in early 2025.
- Birds in some Ukrainian cities have built nests with discarded fiber.

## Vendor landscape (defensive)

| Vendor | System | Notes |
|---|---|---|
| [DroneShield](https://www.droneshield.com/) 🇦🇺/🇺🇸 | RfPatrol, DroneGun | RF defeat |
| [Robin Radar](https://www.robinradar.com/) 🇳🇱 | IRIS | Radar detection |
| [Anduril](https://www.anduril.com/counter-uas) 🇺🇸 | Lattice + Anvil + Roadrunner-M | $20B JIATF-401 contract |
| [Auterion](https://auterion.com/) 🇨🇭 | AuterionOS / Skynode S | EW-resistant autonomy |
| [Bukovel-AD](https://en.wikipedia.org/wiki/Bukovel_(counter_unmanned_aircraft_system)) 🇺🇦 | RF jam + GPS denial | Detection range up to 100 km |
| [Mandat / Grif / Cloud](https://steback.site/storage/files/BUKOVEL,%20MANDAT,%20GRIF,%20CLOUD.pdf) 🇺🇦 | EW family | Ukrainian SpetsTechnoExport |
| [Pantsir-S1](https://en.wikipedia.org/wiki/Pantsir_missile_system) 🇷🇺 | SAM + 30 mm | Now itself a high-priority drone target |
| [Tor-M2](https://en.wikipedia.org/wiki/Tor_missile_system) 🇷🇺 | SAM | Used vs. drones |
| [Coyote Block 3](https://www.rtx.com/raytheon/what-we-do/integrated-air-and-missile-defense/coyote) 🇺🇸 | Interceptor drone | Raytheon |

## Doctrine references

- US JP 3-85 (Joint Electromagnetic Spectrum Operations)
- NATO MC 0064 (NATO Electronic Warfare Policy)
- [ICDS Estonia — Russia's EW Capabilities to 2025](https://icds.ee/wp-content/uploads/2018/ICDS_Report_Russias_Electronic_Warfare_to_2025.pdf)
- [Hudson — The Fall and Rise of Russian EW](https://www.hudson.org/national-security-defense/the-fall-and-rise-of-russian-electronic-warfare)
- [Army Univ. Press — Russian Adaptation Lessons](https://www.armyupress.army.mil/Portals/7/military-review/Archives/English/so25/Lessons-from-Ukraine/Lessons-from-Ukraine-ua.pdf)
- [Ifri — Mapping the MilTech War](https://www.ifri.org/en/studies/mapping-miltech-war-eight-lessons-ukraines-battlefield)
