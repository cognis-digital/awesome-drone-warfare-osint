# ⚖ Disclaimer & Ethical Charter

## Purpose

`awesome-drone-warfare-osint` is a **forensic, journalistic, academic, and
sanctions-enforcement** resource. Its single mission is to make publicly
documented, post-strike hardware findings searchable, citable, and reproducible.

## What this repo IS

- ✅ An aggregation of **already-public** forensic records released by
  governments (GUR/HUR Ukraine, NACP Ukraine), inter-governmental and
  non-governmental research organizations (Conflict Armament Research,
  IISS, RUSI, CSIS, KSE Institute, ISIS-online), and credentialed
  journalism (Reuters, Schemes, Kyiv Independent, SwissInfo, Bellingcat).
- ✅ A **machine-readable** mirror of that public record, with a schema that
  enables academic citation and sanctions cross-referencing
  (OpenSanctions, EU CFSP, OFAC, UK OFSI).
- ✅ A neutral methodology: Russian *and* Ukrainian platforms are documented
  with **the same schema**, because forensic transparency must cut both ways.

## What this repo IS NOT

- ❌ **Not a build guide.** No firmware, no CAD/STEP files, no PCB gerbers,
  no flight-controller binaries, no jammer schematics, no RF spoofing code.
- ❌ **Not operational intelligence.** No live tracking, no operator PII,
  no current-deployment locations.
- ❌ **Not a weapons catalog for procurement.** Pricing rows refer only to
  publicly reported per-unit estimates from open journalism (e.g.
  [Shahed cost analysis](https://phenomenalworld.org/analysis/cost-of-a-shahed/)).
- ❌ **Not a circumvention of export controls.** Aggregating public data
  does not, and is not intended to, bypass EAR, ITAR, EU Dual-Use Regulation
  2021/821, UK Strategic Export Control, or equivalent national regimes.

## Inclusion criteria — every row must satisfy ALL of:

1. **Public source.** A `source_url` to a page or PDF that was already public
   at the time of inclusion.
2. **Post-strike forensics only.** Hardware is identified from wreckage or
   captured units — never from pre-strike intelligence.
3. **No operational PII.** Operators, victims, and personally identifying
   information are excluded; incident records use ACLED-style anonymization.
4. **Reproducible.** A third party using `source_url` must be able to verify
   the row in under five minutes.

## Inclusion criteria — every row must NOT contain:

1. Firmware, exploit code, jammer schematics, or weaponizable CAD.
2. Personal data of military personnel, prisoners, or civilians.
3. Identifiers that enable battlefield targeting of any party.
4. Material under active take-down requests from primary sources.

## Take-down policy

If you are an authorized representative of:

- A primary source that wishes to update or retract a referenced record;
- A company named in `manufacturers.csv` that has new compliance evidence;
- A government agency with a lawful request;

… open a confidential issue using the **`takedown`** template or email the
maintainers (address in `MAINTAINERS.md`). We respond within **72 hours**
and document every action transparently in `TAKEDOWNS.md`.

## Neutrality clause

The maintainers do not endorse any party to any conflict. The dataset
records what is **demonstrable from public forensic evidence**. Where
evidence is contested, both readings are recorded in `notes`.

## Legal posture

- **Data license:** CC BY 4.0 — attribution is mandatory.
- **Code license:** MIT.
- **Jurisdiction of redistribution:** Each redistributor is responsible
  for compliance with their own jurisdiction's export-control,
  sanctions, and press-freedom law.
- **Compiling vs. exporting:** Compiling public information into a
  database is generally protected research/journalism in the EU
  (Charter Art. 11), US (1st Amendment), UK (Art. 10 ECHR), and
  Ukraine. Redistributing the **same** information into a jurisdiction
  that has export-controlled the underlying technology remains the
  redistributor's responsibility.

## Acknowledgement

This dataset would not exist without the brave forensic work of the
**Defence Intelligence of Ukraine (HUR/GUR)**, the **National Agency
on Corruption Prevention (NACP) of Ukraine**, **Conflict Armament
Research**, **RUSI**, **IISS**, **KSE Institute**, **ISIS-online**, and
the open-source intelligence community at large.

— *The maintainers*
