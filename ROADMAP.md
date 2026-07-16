# Roadmap

Direction for the dataset and its tooling. This is a living document — proposals
and corrections are welcome via a Discussion or issue. Nothing here is a
commitment to a date; items are grouped by horizon and rough dependency order.

## Near-term (next few releases)

* **Analytics coverage** — extend the `osint_analytics` primitives with:
  * dual-use exposure (`is_dual_use` roll-ups per platform / per country),
  * manufacturer-level concentration (top suppliers per platform),
  * category concentration (which functional categories are single-sourced).
* **Richer CSV/JSON exports** — a `query.py export` subcommand that writes a
  filtered slice of any table to a file, with column selection.
* **CLI ergonomics** — `--limit`/`--sort` flags on the search commands;
  `--data-dir` to point the CLI at an alternate dataset snapshot.
* **Test depth** — property-based tests for the JSON-list round-trips and the
  CSV renderer; golden-file tests for the analytics against a frozen fixture.
* **Docs** — per-table field dictionaries generated from the JSON Schemas so the
  column reference can never drift from the data.

## Mid-term

* **Supply-chain graph** — promote `supply_chain_edges.csv` into a first-class
  queryable graph (path queries: "which manufacturers reach platform X, and via
  which intermediaries?") with an exportable node/edge format.
* **Sanctions cross-reference** — optional enrichment that joins manufacturers to
  public sanctions-list identifiers at load time, behind a clearly-marked
  provenance flag.
* **Time series** — capture `last_verified` history so the dataset can answer
  "when did component Y first appear in platform X?" and chart component churn.
* **Confidence scoring** — a per-row confidence field derived from source count /
  source tier, surfaced in query output.
* **Packaging** — publish the query CLI as an installable console tool with a
  pinned, minimal dependency set.

## Long-term

* **Multi-theater normalization** — a consistent platform taxonomy across the
  Ukraine, Red Sea, Sudan, and Indo-Pacific corpora so cross-theater comparisons
  are apples-to-apples.
* **Federated corrections** — a lightweight, provenance-preserving way for
  external researchers to submit and review row corrections at scale.
* **Reproducible releases** — versioned, checksummed dataset snapshots with a
  DOI per release for citation stability.
* **Interoperability** — first-class export to the common threat-intel and
  data-analysis interchange formats already referenced in `INTEGRATIONS.md`.

## Non-goals

Consistent with [`DISCLAIMER.md`](DISCLAIMER.md), the project will **not** host or
generate: weapon-build instructions, flight/guidance firmware, jamming or
counter-measure implementations, CAD/geometry for munitions, or anything whose
primary use is offensive. The dataset documents publicly identified hardware for
forensic, journalistic, academic, and sanctions-enforcement purposes only.
