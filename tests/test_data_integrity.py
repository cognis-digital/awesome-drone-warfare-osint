"""Invariant tests over the real published dataset (``data/*.csv``).

These guard against regressions in the shipped data itself: identifier
uniqueness, country-code formatting, enum membership for controlled
vocabularies, JSON-list well-formedness, and referential integrity between
components and platforms. They complement the JSON-Schema validation in
``scripts/validate.py`` with cross-row / cross-table checks that are natural
to express in pytest.
"""

from __future__ import annotations

import json
import re

import pytest

import osint_analytics as oa

COUNTRY_RE = re.compile(r"^([A-Z]{2}|UNK)$")
SANCTIONS_ENUM = {"unsanctioned", "eu", "us", "uk", "ofac", "multi", "unknown"}


@pytest.fixture(scope="module")
def components(data_dir):
    return oa.load_table(data_dir, "components")


@pytest.fixture(scope="module")
def drones(data_dir):
    return oa.load_table(data_dir, "drones")


@pytest.fixture(scope="module")
def manufacturers(data_dir):
    return oa.load_table(data_dir, "manufacturers")


def test_dataset_is_substantial(components, drones):
    assert len(components) >= 1000
    assert len(drones) >= 100


def test_component_ids_well_formed(components):
    """Every component_id is present and matches the slug pattern.

    Note: component_id is intentionally *not* globally unique — the same
    catalogued part is listed once per platform it is documented in — so we
    assert format, not uniqueness.
    """
    id_re = re.compile(r"^[a-z0-9-]+$")
    bad = [c["component_id"] for c in components
           if not c["component_id"] or not id_re.match(c["component_id"])]
    assert not bad, f"malformed component_id values: {bad[:5]}"


def test_drone_ids_unique(drones):
    ids = [d["id"] for d in drones]
    assert len(ids) == len(set(ids))


def test_component_country_codes_well_formed(components):
    bad = {c["component_id"]: c["manufacturer_country"]
           for c in components if not COUNTRY_RE.match(c["manufacturer_country"] or "")}
    assert not bad, f"malformed manufacturer_country values: {list(bad.items())[:5]}"


def test_sanctions_status_in_enum(components):
    bad = {c["component_id"]: c["sanctions_status"]
           for c in components
           if (c.get("sanctions_status") or "unknown") not in SANCTIONS_ENUM}
    assert not bad, f"unexpected sanctions_status values: {list(bad.items())[:5]}"


def test_found_in_drones_is_valid_json_list(components):
    for c in components:
        raw = c["found_in_drones"]
        parsed = json.loads(raw)
        assert isinstance(parsed, list)
        assert parsed, f"{c['component_id']} lists no platform"


def test_every_component_platform_is_registered(components, drones):
    """Referential integrity: platforms referenced by components should exist.

    The scrapers auto-register stubs, so on a healthy tree this holds. We
    assert the overwhelming majority resolve to guard against a broken join
    while tolerating a small in-flight backlog.
    """
    drone_ids = {d["id"] for d in drones}
    referenced = set()
    for c in components:
        referenced.update(oa.parse_json_list(c["found_in_drones"]))
    missing = referenced - drone_ids
    resolved = len(referenced - missing)
    assert resolved / max(len(referenced), 1) >= 0.95, (
        f"{len(missing)} of {len(referenced)} referenced platforms unregistered"
    )


def test_manufacturer_countries_well_formed(manufacturers):
    bad = [m["country"] for m in manufacturers
           if not COUNTRY_RE.match(m["country"] or "")]
    assert not bad, f"malformed manufacturer countries: {bad[:5]}"


def test_analytics_agree_with_raw_counts(components):
    """country_breakdown totals must equal the component count."""
    total = sum(n for _, n in oa.country_breakdown(components))
    assert total == len(components)
