---
name: event-ledger
description: Append-only cryptographic event store. Seals clinical telemetry and biomarker observations with SHA-256 hash chaining to ensure tamper-proof history. Adapted from PLSI (MIT License).
---

# Cryptographic Event Ledger Skill

Use this skill whenever logging new lab observations or verifying data chain integrity.

### How to Run
Verify chain integrity:
```bash
.venv/bin/python3 .agents/skills/event-ledger/scripts/event_ledger.py --ledger telemetry/logs/clinical_events.jsonl --verify
```

Record an event:
```bash
.venv/bin/python3 .agents/skills/event-ledger/scripts/event_ledger.py --ledger telemetry/logs/clinical_events.jsonl --record '{"event": "LAB_OBSERVATION", "ldl_c": 64.0}'
```
