# Drone family tree

```mermaid
graph TD
  HESA[HESA Shahed Aviation 🇮🇷] --> S131[Shahed-131]
  HESA --> S136[Shahed-136]
  HESA --> S238[Shahed-238]
  S136 -->|tech transfer| GERAN[Geran family 🇷🇺]
  GERAN --> G2[Geran-2 piston]
  GERAN --> G3[Geran-3 jet]
  GERAN --> G4[Geran-4 turbojet 🇨🇳 LX-WP-160]
  GERAN --> G5[Geran-5]

  HESA --> MOHAJER[Mohajer family 🇮🇷]
  HESA --> ARASH[Arash-2]

  HOUTHI[Houthi 🇾🇪] --> SAMAD[Samad-3]
  HOUTHI --> QASEF[Qasef-2K]

  ZALA[ZALA Aero 🇷🇺] --> LANCET1[Lancet-1]
  ZALA --> LANCET3[Lancet-3]
  ZALA --> IZD51[Izdeliye-51/52]

  STC[STC Saint Petersburg 🇷🇺] --> ORLAN10[Orlan-10]
  STC --> ORLAN30[Orlan-30]

  ARDUPILOT[ArduPilot open-source autopilot] --> BABA[Baba-Yaga/Vampire 🇺🇦]
  ARDUPILOT --> BOBER[Bober/Liutyi 🇺🇦]
  ARDUPILOT --> SPIDER[Operation Spider's Web FPVs 🇺🇦]

  WILDH[Wild Hornets 🇺🇦] --> STING[Sting interceptor]
  WILDH --> CARGO[Heavy bombers]
```

The tree omits Western platforms (Switchblade, Bayraktar, Skydio, etc.)
which are catalogued in `data/drones.csv` but not central to the
sanctions-evasion narrative this dataset documents.
