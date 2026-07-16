"""Shared pytest fixtures and path setup for the test suite.

Adds the repository root and ``scripts/`` to ``sys.path`` so the top-level
modules (``query``, ``livesearch``, ``osint_analytics``) and the maintenance
scripts (``validate``, ``headline_numbers``) can be imported directly, and
exposes small in-memory component/drone fixtures used by the analytics tests.
"""

from __future__ import annotations

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
for _p in (ROOT, SCRIPTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

DATA_DIR = os.path.join(ROOT, "data")


@pytest.fixture(scope="session")
def data_dir() -> str:
    """Absolute path to the repository's ``data/`` directory."""
    return DATA_DIR


@pytest.fixture()
def sample_components() -> list[dict]:
    """A small, hand-built components table covering the interesting cases.

    Includes multiple origin countries, a shared platform, a blank country
    (normalised to UNK), a multi-platform component, and a spread of
    sanctions statuses.
    """
    return [
        {"component_id": "c1", "manufacturer_country": "US",
         "sanctions_status": "us", "found_in_drones": '["alpha", "bravo"]'},
        {"component_id": "c2", "manufacturer_country": "US",
         "sanctions_status": "unsanctioned", "found_in_drones": '["alpha"]'},
        {"component_id": "c3", "manufacturer_country": "CN",
         "sanctions_status": "unknown", "found_in_drones": '["alpha"]'},
        {"component_id": "c4", "manufacturer_country": "cn",
         "sanctions_status": "unknown", "found_in_drones": '["bravo"]'},
        {"component_id": "c5", "manufacturer_country": "",
         "sanctions_status": "unknown", "found_in_drones": '["alpha"]'},
    ]
