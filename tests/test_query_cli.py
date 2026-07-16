"""End-to-end tests for the ``query`` command-line interface.

These exercise the real dataset through ``query.main(argv)``, capturing
stdout and asserting on observable behaviour (counts, formats, new
analytical subcommands). Assertions are written to be robust to ongoing
dataset growth (lower bounds, structural checks) rather than brittle exact
counts.
"""

from __future__ import annotations

import csv
import io
import json

import pytest

import query


def run(capsys, argv):
    """Invoke the CLI and return (exit_code, stdout_text)."""
    code = query.main(argv)
    out = capsys.readouterr().out
    return code, out


# --------------------------------------------------------------------------- #
# selftest + backward compatibility
# --------------------------------------------------------------------------- #
def test_selftest_passes(capsys):
    code, out = run(capsys, ["--selftest"])
    assert code == 0
    assert "selftest passed" in out


def test_legacy_json_flag_still_works(capsys):
    code, out = run(capsys, ["--json", "stats"])
    assert code == 0
    payload = json.loads(out)
    assert payload["drones"] >= 100
    assert payload["components"] >= 1000


def test_jlist_helper_backward_compatible():
    assert query._jlist('["x", "y"]') == ["x", "y"]
    assert query._jlist("") == []


# --------------------------------------------------------------------------- #
# stats
# --------------------------------------------------------------------------- #
def test_stats_table_output(capsys):
    code, out = run(capsys, ["stats"])
    assert code == 0
    assert "components:" in out
    assert "distinct manufacturers:" in out


def test_stats_csv_output(capsys):
    code, out = run(capsys, ["--format", "csv", "stats"])
    assert code == 0
    rows = list(csv.DictReader(io.StringIO(out)))
    assert rows and set(rows[0]) == {"country", "components"}
    # counts are integers and monotonically non-increasing (top-N sorted)
    counts = [int(r["components"]) for r in rows]
    assert counts == sorted(counts, reverse=True)


# --------------------------------------------------------------------------- #
# component / manufacturer / country / drone search
# --------------------------------------------------------------------------- #
def test_component_search_finds_matches(capsys):
    code, out = run(capsys, ["--json", "component", "servo"])
    assert code == 0
    rows = json.loads(out)
    assert isinstance(rows, list) and len(rows) >= 1
    assert all("servo" in (r["name"] + r["manufacturer"]).lower()
               or "servo" in r.get("part", "").lower() for r in rows)


def test_component_search_no_match_is_empty_json(capsys):
    code, out = run(capsys, ["--json", "component", "zzz-no-such-part-xyzzy"])
    assert code == 0
    assert json.loads(out) == []


def test_country_filter_matches_requested_code(capsys):
    code, out = run(capsys, ["--json", "country", "us"])
    assert code == 0
    rows = json.loads(out)
    assert len(rows) >= 1  # dataset has US-origin components


def test_drones_role_filter(capsys):
    code, out = run(capsys, ["--json", "drones", "--role", "loitering"])
    assert code == 0
    rows = json.loads(out)
    assert rows and all("loitering" in r["role"].lower() for r in rows)


# --------------------------------------------------------------------------- #
# new analytical subcommands
# --------------------------------------------------------------------------- #
def test_chokepoint_shares_sum_to_100(capsys):
    code, out = run(capsys, ["--json", "chokepoint", "geran-4-uav"])
    assert code == 0
    rows = json.loads(out)
    assert rows, "expected the seed platform to have documented components"
    total = round(sum(float(r["share_pct"]) for r in rows))
    assert total == 100
    # sorted by component count descending
    counts = [r["components"] for r in rows]
    assert counts == sorted(counts, reverse=True)


def test_chokepoint_unknown_platform_empty(capsys):
    code, out = run(capsys, ["--json", "chokepoint", "no-such-platform-xyz"])
    assert code == 0
    assert json.loads(out) == []


def test_exposure_lists_platforms_for_country(capsys):
    code, out = run(capsys, ["--json", "exposure", "US"])
    assert code == 0
    rows = json.loads(out)
    assert rows, "US parts should appear in at least one platform"
    assert all(r["components_from_country"] >= 1 for r in rows)
    counts = [r["components_from_country"] for r in rows]
    assert counts == sorted(counts, reverse=True)


def test_sanctions_breakdown_csv(capsys):
    code, out = run(capsys, ["--format", "csv", "sanctions"])
    assert code == 0
    rows = list(csv.DictReader(io.StringIO(out)))
    assert rows and set(rows[0]) == {"sanctions_status", "components", "share_pct"}
    total = round(sum(float(r["share_pct"]) for r in rows))
    assert total == 100


def test_sanctions_scoped_country(capsys):
    code, out = run(capsys, ["--json", "sanctions", "--country", "CN"])
    assert code == 0
    rows = json.loads(out)
    # every documented status count is a positive integer
    assert rows and all(r["components"] >= 1 for r in rows)


# --------------------------------------------------------------------------- #
# format resolution helper
# --------------------------------------------------------------------------- #
def test_fmt_resolution_precedence():
    ns = query.argparse.Namespace(format="csv", json=True)
    assert query._fmt(ns) == "csv"           # explicit --format wins
    ns = query.argparse.Namespace(format=None, json=True)
    assert query._fmt(ns) == "json"          # legacy flag
    ns = query.argparse.Namespace(format=None, json=False)
    assert query._fmt(ns) == "table"         # default


def test_unknown_subcommand_errors(capsys):
    with pytest.raises(SystemExit):
        query.main(["frobnicate"])
