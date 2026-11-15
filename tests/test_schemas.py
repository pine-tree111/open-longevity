#!/usr/bin/env python3
"""
Unit tests to validate telemetry schema files are valid JSON.
"""

import json
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "telemetry" / "schemas"


def test_biomarker_schema_validity():
    schema_path = SCHEMA_DIR / "biomarker_schema.json"
    assert schema_path.exists()
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["title"] == "BiomarkerObservation"
    assert "required" in schema
    assert "marker" in schema["required"]


def test_daily_log_schema_validity():
    schema_path = SCHEMA_DIR / "daily_log_schema.json"
    assert schema_path.exists()
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["title"] == "DailyMetricLog"
    assert "date" in schema["required"]
