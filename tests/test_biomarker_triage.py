#!/usr/bin/env python3
"""
Unit tests for Open-Longevity Biomarker Triage Engine.
"""

import sys
from pathlib import Path
import pytest

# Add skill script directory to sys.path
SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "biomarker-triage" / "scripts"
sys.path.insert(0, str(SKILL_DIR))

import triage_engine


def test_triage_optimal_profile():
    test_data = {
        "baseline_biomarkers": {
            "lipids": {
                "apob_mg_dl": 52.0,
                "ldl_c_mg_dl": 62.0,
                "triglycerides_mg_dl": 65.0,
                "hdl_c_mg_dl": 60.0,
            },
            "glycemic_and_metabolic": {
                "fasting_glucose_mg_dl": 84.0,
                "hba1c_percent": 5.1,
                "two_hour_ogtt_mg_dl": 105.0,
            },
            "cardiovascular_and_inflammatory": {
                "hs_crp_mg_l": 0.3,
            },
            "organ_safety_and_renal": {
                "alt_u_l": 18.0,
            },
        }
    }
    report = triage_engine.run_triage(test_data)
    assert report["summary"]["critical_kill_vectors_count"] == 0
    assert report["summary"]["suboptimal_count"] == 0
    assert report["summary"]["optimal_count"] >= 7


def test_triage_critical_cardiometabolic_flags():
    test_data = {
        "baseline_biomarkers": {
            "lipids": {
                "apob_mg_dl": 135.0,     # Critical
                "ldl_c_mg_dl": 195.0,     # Critical (>190)
                "triglycerides_mg_dl": 220.0,
                "hdl_c_mg_dl": 35.0,      # Ratio > 6.0 (Critical)
            },
            "glycemic_and_metabolic": {
                "fasting_glucose_mg_dl": 115.0, # Prediabetes
                "hba1c_percent": 5.9,          # Prediabetes
                "two_hour_ogtt_mg_dl": 185.0,  # Severe IGT (Critical)
            },
            "cardiovascular_and_inflammatory": {
                "hs_crp_mg_l": 3.8,      # High inflammation
            },
            "organ_safety_and_renal": {
                "alt_u_l": 55.0,         # Elevated transaminases
            },
        }
    }
    report = triage_engine.run_triage(test_data)
    assert report["summary"]["critical_kill_vectors_count"] >= 5
    critical_markers = [item["marker"] for item in report["critical_kill_vectors"]]
    assert "ApoB" in critical_markers
    assert "LDL-C" in critical_markers
    assert "2-Hr OGTT" in critical_markers
