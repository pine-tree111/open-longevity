---
name: healthspan-modeling
description: Gompertz survival and actuarial hazard model. Calculates expected remaining healthspan, survival curves, and milestone probabilities based on biological age and proportional hazard ratio shifts.
---

# Healthspan Modeling Skill

Use this skill to model longevity trajectories and quantify years gained from risk-reduction interventions.

### How to Run
```bash
.venv/bin/python3 .agents/skills/healthspan-modeling/scripts/healthspan_sim.py --age 35 --hr 0.78 --shift -3.5 --source "ApoB Eradication + Exercise"
```
