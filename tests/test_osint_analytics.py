"""Unit tests for the pure analytics primitives in ``osint_analytics``."""

from __future__ import annotations

import csv
import io

import pytest

import osint_analytics as oa


# --------------------------------------------------------------------------- #
# parse_json_list
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "raw, expected",
    [
        ('["a", "b"]', ["a", "b"]),
        ("[]", []),
        ("", []),
        (None, []),
        ("not json at all", []),
        ('{"not": "a list"}', []),
        ('"a bare string"', []),
        ("[1, 2, 3]", ["1", "2", "3"]),  # non-str items are stringified
    ],
)
def test_parse_json_list(raw, expected):
    assert oa.parse_json_list(raw) == expected


def test_parse_json_list_never_raises_on_garbage():
    for junk in ("[unterminated", "\x00\x01", "[[[", "true", "42"):
        assert isinstance(oa.parse_json_list(junk), list)


# --------------------------------------------------------------------------- #
# country_breakdown
# --------------------------------------------------------------------------- #
def test_country_breakdown_all_components(sample_components):
    result = oa.country_breakdown(sample_components)
    # US=2, CN=2 (one lower-cased, normalised), UNK=1 (blank normalised)
    assert result == [("CN", 2), ("US", 2), ("UNK", 1)]


def test_country_breakdown_sorted_by_count_then_code(sample_components):
    counts = [n for _, n in oa.country_breakdown(sample_components)]
    assert counts == sorted(counts, reverse=True)


def test_country_breakdown_scoped_to_platform(sample_components):
    # platform "alpha" contains c1(US), c2(US), c3(CN), c5(UNK)
    result = oa.country_breakdown(sample_components, drone_id="alpha")
    assert result == [("US", 2), ("CN", 1), ("UNK", 1)]


def test_country_breakdown_unknown_platform_is_empty(sample_components):
    assert oa.country_breakdown(sample_components, drone_id="does-not-exist") == []


def test_country_breakdown_empty_input():
    assert oa.country_breakdown([]) == []


# --------------------------------------------------------------------------- #
# sanctions_breakdown
# --------------------------------------------------------------------------- #
def test_sanctions_breakdown_all(sample_components):
    result = dict(oa.sanctions_breakdown(sample_components))
    assert result == {"unknown": 3, "us": 1, "unsanctioned": 1}


def test_sanctions_breakdown_scoped_to_country(sample_components):
    # both CN rows have unknown status; country match is case-insensitive
    assert oa.sanctions_breakdown(sample_components, country="cn") == [("unknown", 2)]


def test_sanctions_breakdown_missing_status_defaults_unknown():
    rows = [{"manufacturer_country": "US", "found_in_drones": "[]"}]
    assert oa.sanctions_breakdown(rows) == [("unknown", 1)]


# --------------------------------------------------------------------------- #
# platform_exposure
# --------------------------------------------------------------------------- #
def test_platform_exposure_counts_per_drone(sample_components):
    # US parts: c1 in {alpha,bravo}, c2 in {alpha}  -> alpha=2, bravo=1
    assert oa.platform_exposure(sample_components, "US") == [("alpha", 2), ("bravo", 1)]


def test_platform_exposure_case_insensitive(sample_components):
    # c3 (CN) in alpha, c4 (cn) in bravo -> one each
    assert oa.platform_exposure(sample_components, "cn") == [("alpha", 1), ("bravo", 1)]


def test_platform_exposure_no_such_country(sample_components):
    assert oa.platform_exposure(sample_components, "FR") == []


# --------------------------------------------------------------------------- #
# to_csv
# --------------------------------------------------------------------------- #
def test_to_csv_roundtrips_through_reader():
    rows = [{"a": "1", "b": "x"}, {"a": "2", "b": "y"}]
    text = oa.to_csv(rows, ["a", "b"])
    parsed = list(csv.DictReader(io.StringIO(text)))
    assert parsed == rows


def test_to_csv_header_and_column_subset():
    rows = [{"a": "1", "b": "2", "c": "3"}]
    text = oa.to_csv(rows, ["a", "c"])  # 'b' omitted
    header = text.splitlines()[0]
    assert header == "a,c"
    assert "2" not in text  # dropped column's value is gone


def test_to_csv_missing_key_is_blank():
    text = oa.to_csv([{"a": "1"}], ["a", "b"])
    row = list(csv.DictReader(io.StringIO(text)))[0]
    assert row == {"a": "1", "b": ""}


# --------------------------------------------------------------------------- #
# load_table against the real dataset
# --------------------------------------------------------------------------- #
def test_load_table_reads_real_components(data_dir):
    comps = oa.load_table(data_dir, "components")
    assert len(comps) > 1000
    assert "manufacturer_country" in comps[0]
    assert "found_in_drones" in comps[0]
