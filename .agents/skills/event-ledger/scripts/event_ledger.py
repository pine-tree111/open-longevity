#!/usr/bin/env python3
"""
Immutable Event-Sourced Ledger & Audit Trail.

Adapted from the open-source PLSI architecture (https://github.com/Insilico-org/plsi)
under the MIT License.

Implements an append-only cryptographic event store for clinical telemetry
and biomarker observations:
- Cryptographic hash chaining: Each event seals the SHA-256 hash of the previous event.
- Non-destructive mutations: Historical records are never modified in-place.
- Retraction & Revision Semantics: Corrections are recorded as new RETRACT or REVISE events.
- Verification Engine: Validates the integrity of the entire chain to detect tampering.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple
import uuid
from pydantic import BaseModel, Field

GENESIS_HASH = "0" * 64


class LedgerEvent(BaseModel):
    event_id: str
    timestamp: str
    event_type: Literal["RECORD", "REVISE", "RETRACT"]
    target_event_id: Optional[str] = None
    reason: Optional[str] = None
    payload: dict[str, Any]
    parent_hash: str
    event_hash: str


def compute_event_hash(
    timestamp: str,
    event_type: str,
    target_id: Optional[str],
    parent_hash: str,
    payload: dict[str, Any],
) -> str:
    """Compute deterministic SHA-256 hash for an event."""
    serialized = json.dumps(payload, sort_keys=True)
    raw = f"{timestamp}|{event_type}|{target_id or ''}|{parent_hash}|{serialized}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class EventLedger:
    """Append-only cryptographic event ledger."""

    def __init__(self, ledger_file: Path | str) -> None:
        self.ledger_path = Path(ledger_file)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.touch()

    def _read_all(self) -> List[LedgerEvent]:
        events: List[LedgerEvent] = []
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str:
                    events.append(LedgerEvent.model_validate_json(line_str))
        return events

    def _append(self, event: LedgerEvent) -> None:
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")

    def record(self, payload: dict[str, Any]) -> LedgerEvent:
        """Append a new measurement or observation to the ledger."""
        events = self._read_all()
        parent_hash = events[-1].event_hash if events else GENESIS_HASH

        now_iso = datetime.now(timezone.utc).isoformat()
        evt_id = str(uuid.uuid4())
        evt_hash = compute_event_hash(now_iso, "RECORD", None, parent_hash, payload)

        evt = LedgerEvent(
            event_id=evt_id,
            timestamp=now_iso,
            event_type="RECORD",
            target_event_id=None,
            reason=None,
            payload=payload,
            parent_hash=parent_hash,
            event_hash=evt_hash,
        )
        self._append(evt)
        return evt

    def retract(self, target_event_id: str, reason: str) -> LedgerEvent:
        """Retract a previous event without deleting its historical record."""
        events = self._read_all()
        if not any(e.event_id == target_event_id for e in events):
            raise KeyError(f"Target event '{target_event_id}' does not exist in ledger.")

        parent_hash = events[-1].event_hash if events else GENESIS_HASH
        now_iso = datetime.now(timezone.utc).isoformat()
        evt_id = str(uuid.uuid4())
        payload = {"retracted_id": target_event_id, "reason": reason}
        evt_hash = compute_event_hash(now_iso, "RETRACT", target_event_id, parent_hash, payload)

        evt = LedgerEvent(
            event_id=evt_id,
            timestamp=now_iso,
            event_type="RETRACT",
            target_event_id=target_event_id,
            reason=reason,
            payload=payload,
            parent_hash=parent_hash,
            event_hash=evt_hash,
        )
        self._append(evt)
        return evt

    def verify_integrity(self) -> Tuple[bool, str]:
        """Verify the cryptographic hash chain of the entire ledger."""
        events = self._read_all()
        if not events:
            return True, "Ledger is empty (valid)."

        expected_parent = GENESIS_HASH
        for idx, evt in enumerate(events):
            if evt.parent_hash != expected_parent:
                return False, f"Hash chain break at event index {idx} ({evt.event_id}): parent_hash mismatch."

            recomputed = compute_event_hash(
                evt.timestamp,
                evt.event_type,
                evt.target_event_id,
                evt.parent_hash,
                evt.payload,
            )
            if recomputed != evt.event_hash:
                return False, f"Event hash corruption at index {idx} ({evt.event_id}): hash altered."

            expected_parent = evt.event_hash

        return True, f"Ledger integrity verified ({len(events)} events, unbroken chain)."


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage immutable longevity event ledger.")
    parser.add_argument("--ledger", type=str, default="telemetry/logs/events.jsonl", help="Ledger file path")
    parser.add_argument("--verify", action="store_true", help="Verify cryptographic chain integrity")
    parser.add_argument("--record", type=str, help="Record JSON string payload")

    args = parser.parse_args()
    ledger = EventLedger(args.ledger)

    if args.verify:
        ok, msg = ledger.verify_integrity()
        print(f"Status: {'PASS' if ok else 'FAIL'} | {msg}")
    elif args.record:
        payload = json.loads(args.record)
        evt = ledger.record(payload)
        print(f"Recorded event: {evt.event_id} (hash: {evt.event_hash[:16]}...)")


if __name__ == "__main__":
    main()
