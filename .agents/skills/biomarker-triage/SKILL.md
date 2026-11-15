---
name: biomarker-triage
description: Algorithmic blood test triage engine. Evaluates lipids, glycemic metrics, inflammation, and organ markers against consensus longevity thresholds.
---

# Biomarker Triage Skill

Use this skill whenever evaluating a user's blood test results or profile metrics.

### How to Run
Execute using the virtual environment:
```bash
.venv/bin/python3 .agents/skills/biomarker-triage/scripts/triage_engine.py --profile profile/user_profile.yaml
```

### Output Tiers
- **OPTIMAL**: Biological metrics in the top centile for long-term healthspan.
- **SUBOPTIMAL**: Early warning indicators treatable via lifestyle, exercise timing, or nutrition.
- **CRITICAL**: Significant cardiometabolic or organ risk vectors requiring immediate clinical evaluation.
