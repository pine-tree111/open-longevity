---
name: epistemic-guard
description: Anti-hype evidence and scientific integrity auditor. Screens protocol prose for unanchored superlatives, vague wellness claims, and unfalsifiable assertions. Adapted from PLSI (MIT License).
---

# Epistemic Guard Skill

Use this skill whenever generating or reviewing recommendations, protocols, or literature summaries.

### How to Run
```bash
.venv/bin/python3 .agents/skills/epistemic-guard/scripts/epistemic_guard.py --text "Your protocol text to audit"
```

### Enforced Rules:
1. **Anti-Hype Filter**: Superlative claims require a verified citation identifier (PMID, NCT, DOI) in the exact same sentence.
2. **Anti-Woo Filter**: Rejects unquantifiable wellness claims lacking objective biomarker endpoints.
3. **Mandatory Falsifiers**: Hypotheses must define what empirical observation would prove them false.
