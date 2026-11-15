#!/usr/bin/env python3
"""
Unit tests for PLSI-Adapted Cryptographic Event Ledger.
"""

import sys
import tempfile
from pathlib import Path
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "event-ledger" / "scripts"
sys.path.insert(0, str(SKILL_DIR))

import event_ledger


def test_event_ledger_hash_chain_and_retraction():
    with tempfile.TemporaryDirectory() as tmp_dir:
        ledger_path = Path(tmp_dir) / "test_events.jsonl"
        ledger = event_ledger.EventLedger(ledger_path)

        # 1. Record an event
        evt1 = ledger.record({"event": "LAB_REPORT", "ldl_c": 195.0})
        assert evt1.parent_hash == event_ledger.GENESIS_HASH

        # 2. Record a second event (chained)
        evt2 = ledger.record({"event": "PROTOCOL_START", "action": "ROSUVASTATIN_10MG"})
        assert evt2.parent_hash == evt1.event_hash

        # 3. Verify integrity passes
        ok, msg = ledger.verify_integrity()
        assert ok
        assert "2 events, unbroken chain" in msg

        # 4. Retract the first event
        retract_evt = ledger.retract(evt1.event_id, reason="Typo in lab entry")
        assert retract_evt.parent_hash == evt2.event_hash

        # 5. Verify integrity still holds with retraction
        ok, msg = ledger.verify_integrity()
        assert ok


def test_event_ledger_tamper_detection():
    with tempfile.TemporaryDirectory() as tmp_dir:
        ledger_path = Path(tmp_dir) / "test_events.jsonl"
        ledger = event_ledger.EventLedger(ledger_path)

        evt1 = ledger.record({"event": "OBSERVATION", "val": 100})
        evt2 = ledger.record({"event": "OBSERVATION", "val": 200})

        # Tamper with file directly
        with open(ledger_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        tampered_line = lines[0].replace("100", "999")
        with open(ledger_path, "w", encoding="utf-8") as f:
            f.writelines([tampered_line, lines[1]])

        # Verify integrity fails
        ok, msg = ledger.verify_integrity()
        assert not ok
        assert "Event hash corruption" in msg
