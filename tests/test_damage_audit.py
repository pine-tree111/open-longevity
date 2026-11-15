#!/usr/bin/env python3
"""
Unit tests for Structural Damage Audit Engine.
"""

import sys
from pathlib import Path
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "structural-damage-audit" / "scripts"
sys.path.insert(0, str(SKILL_DIR))

import damage_audit


def test_audit_senolytic_apoptosens():
    audit = damage_audit.audit_intervention("dasatinib_quercetin")
    assert audit is not None
    assert "ApoptoSENS" in audit.primary_pillars
    assert audit.is_structural_repair is True


def test_audit_metabolic_distinction():
    audit = damage_audit.audit_intervention("metformin")
    assert audit is not None
    # Metformin is metabolic tweaking, not primary structural lesion repair
    assert audit.is_structural_repair is False
    assert len(audit.primary_pillars) == 0


def test_audit_unknown_intervention():
    audit = damage_audit.audit_intervention("unregistered_compound_xyz")
    assert audit is None
