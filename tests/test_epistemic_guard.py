#!/usr/bin/env python3
"""
Unit tests for PLSI-Adapted Epistemic Guard Engine.
"""

import sys
from pathlib import Path
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "epistemic-guard" / "scripts"
sys.path.insert(0, str(SKILL_DIR))

import epistemic_guard


def test_epistemic_guard_superlative_without_citation():
    text = "This molecule is the only proven solution for reversing arterial stiffness."
    report = epistemic_guard.audit_protocol(text)
    assert not report.passed
    assert any(v.refusal_code == "REFUSAL-SUPERLATIVE" for v in report.violations)


def test_epistemic_guard_superlative_with_citation():
    text = "This molecule is the strongest known inhibitor according to PMID: 31245678."
    report = epistemic_guard.audit_protocol(text)
    assert report.passed
    assert len(report.violations) == 0


def test_epistemic_guard_vague_biohacking():
    text = "After taking this morning elixir, I felt more energetic and it flushes out toxins."
    report = epistemic_guard.audit_protocol(text)
    assert not report.passed
    assert any(v.refusal_code == "REFUSAL-VAGUE" for v in report.violations)


def test_epistemic_guard_falsification_requirement():
    hypotheses = [
        {"hypothesis": "Zone 2 cycling improves mitochondrial cristae density.", "if_false": None}
    ]
    report = epistemic_guard.audit_protocol("Objective protocol text.", hypotheses=hypotheses)
    assert not report.passed
    assert any(v.refusal_code == "REFUSAL-UNFALSIFIABLE" for v in report.violations)
