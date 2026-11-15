#!/usr/bin/env python3
"""
Unit tests for Healthspan Gompertz Model.
"""

import sys
from pathlib import Path
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "healthspan-modeling" / "scripts"
sys.path.insert(0, str(SKILL_DIR))

import healthspan_sim


def test_gompertz_survival_baseline():
    scenarios = [
        healthspan_sim.SurvivalScenario(name="Baseline")
    ]
    res = healthspan_sim.evaluate_survival(current_age=35.0, scenarios=scenarios)
    assert len(res.results) == 1
    baseline = res.results[0]
    # Expected age at death around 80-86 for standard Gompertz beta=0.085
    assert 78.0 <= baseline.expected_age_at_death <= 88.0
    assert 0.0 < baseline.milestones.reach_100 < 0.20


def test_gompertz_intervention_gain():
    scenarios = [
        healthspan_sim.SurvivalScenario(name="Baseline"),
        healthspan_sim.SurvivalScenario(
            name="Cardiometabolic Optimization",
            hazard_ratio=0.75,
            age_shift=-3.0,
            source="Lancet Lipid Meta-Analysis PMID: 12345678"
        ),
    ]
    res = healthspan_sim.evaluate_survival(current_age=35.0, scenarios=scenarios)
    assert len(res.results) == 2
    gains = res.years_gained_vs_baseline["Cardiometabolic Optimization"]
    assert gains > 3.0  # Significant healthspan gain
    assert res.results[1].milestones.reach_90 > res.results[0].milestones.reach_90


def test_source_validation_required():
    with pytest.raises(ValueError, match="modifies baseline hazard: explicit citation is required"):
        healthspan_sim.SurvivalScenario(
            name="Unsubstantiated Biohack",
            hazard_ratio=0.5,
            source=None  # Missing source must fail validation
        )
