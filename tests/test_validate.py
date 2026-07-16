"""Tests for the dataset validation helpers in ``scripts/validate.py``.

Focuses on the pure ``coerce_row`` type-coercion logic (CSV strings -> the
JSON types the schema expects) since that is where subtle bugs would let bad
data through. ``scripts`` is on ``sys.path`` via ``conftest.py``.
"""

from __future__ import annotations

import validate


def test_coerce_decodes_list_fields():
    row = validate.coerce_row("components",
                              {"found_in_drones": '["a", "b"]', "replaceable_with": "[]"})
    assert row["found_in_drones"] == ["a", "b"]
    assert row["replaceable_with"] == []


def test_coerce_bad_list_becomes_empty():
    row = validate.coerce_row("components", {"found_in_drones": "not-json"})
    assert row["found_in_drones"] == []


def test_coerce_boolean_fields():
    assert validate.coerce_row("components", {"is_dual_use": "true"})["is_dual_use"] is True
    assert validate.coerce_row("components", {"is_dual_use": "False"})["is_dual_use"] is False
    assert validate.coerce_row("teardowns", {"is_pdf": "1"})["is_pdf"] is True
    assert validate.coerce_row("teardowns", {"is_pdf": "no"})["is_pdf"] is False


def test_coerce_integer_fields():
    row = validate.coerce_row("drones", {"total_components_documented": "54"})
    assert row["total_components_documented"] == 54
    # non-numeric ints fall back to 0 rather than raising
    bad = validate.coerce_row("drones", {"total_components_documented": "N/A"})
    assert bad["total_components_documented"] == 0


def test_coerce_float_fields_and_blanks():
    row = validate.coerce_row("components", {"price_retail_usd": "12.5"})
    assert row["price_retail_usd"] == 12.5
    blank = validate.coerce_row("components", {"price_retail_usd": ""})
    assert blank["price_retail_usd"] is None


def test_coerce_nullable_blank_becomes_none():
    # 'function' is a nullable-blank field for components
    row = validate.coerce_row("components", {"function": ""})
    assert row["function"] is None


def test_coerce_preserves_non_blank_strings():
    row = validate.coerce_row("components", {"manufacturer": "Acme Corp"})
    assert row["manufacturer"] == "Acme Corp"
