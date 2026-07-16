#!/usr/bin/env python3
"""Analytical primitives for the drone-warfare OSINT dataset.

This module holds the *pure* data-analysis functions that back the
higher-level ``query.py`` command-line interface. Everything here is
standard-library only, side-effect free (no I/O except the explicit
``load_table`` loader), and independently unit-testable — the CLI is a thin
presentation layer on top of these primitives.

The analytics are aimed at the questions export-control, sanctions-compliance
and OSINT teams actually ask of a component/platform dataset:

* **Concentration** — for a single weapon platform, where (by manufacturer
  country) do its documented parts come from?  A platform whose parts are
  overwhelmingly single-origin has a supply-chain choke point.
* **Exposure** — for a country of origin, which platforms depend on its
  parts, and how heavily?  This is the same question from the supplier side
  and quantifies a country's leverage over a weapon programme.
* **Sanctions posture** — how do the documented components break down by
  sanctions status, optionally scoped to one manufacturer country?

All functions operate on ``list[dict]`` rows exactly as produced by
``csv.DictReader`` over ``data/components.csv`` (and friends), so they are
trivial to exercise with small in-memory fixtures.
"""

from __future__ import annotations

import csv
import io
import json
import os
from collections import Counter
from typing import Iterable, Sequence

__all__ = [
    "parse_json_list",
    "load_table",
    "country_breakdown",
    "sanctions_breakdown",
    "platform_exposure",
    "to_csv",
]


def parse_json_list(value: str | None) -> list[str]:
    """Decode a CSV cell that holds a JSON-encoded list of strings.

    The dataset stores multi-valued fields (e.g. ``found_in_drones``) as a
    JSON array inside a single CSV cell. This helper decodes such a cell,
    returning an empty list for blank cells or anything that is not a JSON
    array — it never raises on malformed input.

    >>> parse_json_list('["a", "b"]')
    ['a', 'b']
    >>> parse_json_list('')
    []
    >>> parse_json_list('not json')
    []
    """
    try:
        decoded = json.loads(value or "[]")
    except (json.JSONDecodeError, TypeError):
        return []
    if not isinstance(decoded, list):
        return []
    return [str(item) for item in decoded]


def load_table(data_dir: str, name: str) -> list[dict[str, str]]:
    """Load ``<data_dir>/<name>.csv`` into a list of row dicts.

    Thin wrapper over :class:`csv.DictReader` with UTF-8 decoding. The
    ``name`` argument is the bare table name without extension (e.g.
    ``"components"``).
    """
    path = os.path.join(data_dir, f"{name}.csv")
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _iter_component_countries(
    components: Iterable[dict[str, str]],
    drone_id: str | None,
) -> Iterable[str]:
    """Yield the manufacturer country for each component in scope.

    When ``drone_id`` is given, only components documented inside that
    platform are counted; otherwise every component is counted. A blank or
    missing country is normalised to ``"UNK"``.
    """
    for comp in components:
        if drone_id is not None and drone_id not in parse_json_list(comp.get("found_in_drones")):
            continue
        yield (comp.get("manufacturer_country") or "UNK").upper()


def country_breakdown(
    components: Sequence[dict[str, str]],
    drone_id: str | None = None,
) -> list[tuple[str, int]]:
    """Count documented components per manufacturer country.

    Returns ``(country_code, count)`` pairs sorted by count descending, then
    country code ascending for stable, deterministic ordering. When
    ``drone_id`` is provided the tally is restricted to components documented
    inside that platform, which surfaces single-origin supply-chain choke
    points for a specific weapon system.
    """
    tally = Counter(_iter_component_countries(components, drone_id))
    return sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))


def sanctions_breakdown(
    components: Sequence[dict[str, str]],
    country: str | None = None,
) -> list[tuple[str, int]]:
    """Break the components down by ``sanctions_status``.

    Returns ``(status, count)`` pairs sorted by count descending, then status
    ascending. When ``country`` is supplied (a two-letter code, case
    insensitive) only components whose manufacturer country matches are
    counted, which answers "how sanctioned is the flow of parts from country
    X?".
    """
    wanted = country.upper() if country else None
    tally: Counter[str] = Counter()
    for comp in components:
        if wanted is not None and (comp.get("manufacturer_country") or "").upper() != wanted:
            continue
        tally[(comp.get("sanctions_status") or "unknown").lower()] += 1
    return sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))


def platform_exposure(
    components: Sequence[dict[str, str]],
    country: str,
) -> list[tuple[str, int]]:
    """Quantify a country's leverage over each weapon platform.

    For manufacturer country ``country`` (two-letter code, case insensitive),
    count how many of that country's documented components appear in each
    platform. Returns ``(drone_id, count)`` pairs sorted by count descending,
    then drone id ascending. A high count means the platform is heavily
    dependent on parts from that country.
    """
    wanted = country.upper()
    tally: Counter[str] = Counter()
    for comp in components:
        if (comp.get("manufacturer_country") or "").upper() != wanted:
            continue
        for drone_id in parse_json_list(comp.get("found_in_drones")):
            tally[drone_id] += 1
    return sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))


def to_csv(rows: Sequence[dict[str, object]], cols: Sequence[str]) -> str:
    """Render ``rows`` as an RFC-4180 CSV string with ``cols`` as the header.

    Only the columns in ``cols`` are emitted, in that order; missing keys are
    written as empty cells. The output uses ``\\r\\n`` line terminators per the
    CSV standard and is safe to write straight to stdout or a file.
    """
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(cols), extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({c: row.get(c, "") for c in cols})
    return buffer.getvalue()
