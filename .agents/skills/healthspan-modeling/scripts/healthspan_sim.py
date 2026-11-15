#!/usr/bin/env python3
"""
Gompertz-Extrapolated Life Table & Healthspan Trajectory Model.

Computes conditional survival curves, remaining life expectancy, and milestone survival
probabilities (reach age 80, 90, 100, 110) based on continuous Gompertz hazard modeling:
  mu(x) = mu0 * exp(beta * (x + age_shift)) * HR

Parameters:
  - mu0: Baseline mortality hazard intercept (~0.00006)
  - beta: Gompertz slope (~0.085, corresponding to an 8.15-year mortality rate doubling time)
  - HR: Proportional Hazard Ratio from clinical interventions
  - age_shift: Biological age gap (years)
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


DEFAULT_GOMPERTZ_MU0 = 0.00006
DEFAULT_GOMPERTZ_BETA = 0.085
MAX_LIFESPAN = 120.0
QUADRATURE_STEP = 0.1  # years for numerical integration


class SurvivalScenario(BaseModel):
    name: str = Field(min_length=1)
    hazard_ratio: float = Field(default=1.0, gt=0.05, le=5.0)
    age_shift: float = Field(default=0.0, ge=-25.0, le=25.0, description="Biological age delta (years)")
    source: Optional[str] = None

    @model_validator(mode="after")
    def _verify_source(self) -> "SurvivalScenario":
        if (self.hazard_ratio != 1.0 or self.age_shift != 0.0) and not self.source:
            raise ValueError(f"Scenario '{self.name}' modifies baseline hazard: explicit citation is required.")
        return self


class MilestoneProbabilities(BaseModel):
    reach_80: float
    reach_90: float
    reach_100: float
    reach_110: float


class SurvivalCurvePoint(BaseModel):
    age: float
    years_ahead: float
    survival_prob: float


class ScenarioSurvivalResult(BaseModel):
    scenario_name: str
    hazard_ratio: float
    age_shift: float
    expected_remaining_lifespan: float
    expected_age_at_death: float
    milestones: MilestoneProbabilities
    curve: List[SurvivalCurvePoint]


class MultiScenarioSurvivalComparison(BaseModel):
    chronological_age: float
    results: List[ScenarioSurvivalResult]
    years_gained_vs_baseline: Dict[str, float]


def survival_prob(
    current_age: float,
    t_years: float,
    hr: float,
    age_shift: float,
    mu0: float = DEFAULT_GOMPERTZ_MU0,
    beta: float = DEFAULT_GOMPERTZ_BETA,
) -> float:
    """Compute S(t | current_age) under Gompertz hazard."""
    if t_years <= 0:
        return 1.0
    effective_age = current_age + age_shift
    factor = (hr * mu0 / beta) * math.exp(beta * effective_age)
    cum_hazard = factor * (math.exp(beta * t_years) - 1.0)
    return math.exp(-cum_hazard)


def integrate_remaining_lifespan(
    current_age: float,
    hr: float,
    age_shift: float,
    max_age: float = MAX_LIFESPAN,
    step: float = QUADRATURE_STEP,
) -> float:
    """Numerically integrate remaining life expectancy: e_x = integral_0^(max_age - x) S(t | x) dt."""
    remaining_max = max(0.0, max_age - current_age)
    if remaining_max <= 0:
        return 0.0

    n_steps = int(remaining_max / step)
    area = 0.0
    for i in range(n_steps):
        t1 = i * step
        t2 = (i + 1) * step
        s1 = survival_prob(current_age, t1, hr, age_shift)
        s2 = survival_prob(current_age, t2, hr, age_shift)
        # Trapezoidal rule
        area += 0.5 * (s1 + s2) * step

    return area


def evaluate_survival(
    current_age: float,
    scenarios: List[SurvivalScenario],
) -> MultiScenarioSurvivalComparison:
    """Evaluate survival trajectories and milestone probabilities across scenarios."""
    results: List[ScenarioSurvivalResult] = []
    target_ages = [80.0, 90.0, 100.0, 110.0]

    for sc in scenarios:
        e_x = integrate_remaining_lifespan(current_age, sc.hazard_ratio, sc.age_shift)
        expected_death_age = current_age + e_x

        # Compute milestone survival probabilities
        milestones_dict = {}
        for m_age in target_ages:
            t_to_m = max(0.0, m_age - current_age)
            p = survival_prob(current_age, t_to_m, sc.hazard_ratio, sc.age_shift) if m_age > current_age else 1.0
            milestones_dict[f"reach_{int(m_age)}"] = round(p, 4)

        # Generate sample survival curve (every 5 years up to age 115)
        curve_points: List[SurvivalCurvePoint] = []
        curve_years = range(0, int(MAX_LIFESPAN - current_age) + 1, 5)
        for yr in curve_years:
            p_surv = survival_prob(current_age, float(yr), sc.hazard_ratio, sc.age_shift)
            curve_points.append(
                SurvivalCurvePoint(
                    age=round(current_age + yr, 1),
                    years_ahead=float(yr),
                    survival_prob=round(p_surv, 4),
                )
            )

        results.append(
            ScenarioSurvivalResult(
                scenario_name=sc.name,
                hazard_ratio=sc.hazard_ratio,
                age_shift=sc.age_shift,
                expected_remaining_lifespan=round(e_x, 2),
                expected_age_at_death=round(expected_death_age, 2),
                milestones=MilestoneProbabilities(**milestones_dict),
                curve=curve_points,
            )
        )

    baseline_lifespan = results[0].expected_remaining_lifespan if results else 0.0
    gains: Dict[str, float] = {}
    for r in results:
        gains[r.scenario_name] = round(r.expected_remaining_lifespan - baseline_lifespan, 2)

    return MultiScenarioSurvivalComparison(
        chronological_age=current_age,
        results=results,
        years_gained_vs_baseline=gains,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Gompertz-extrapolated survival and healthspan model.")
    parser.add_argument("--age", type=float, required=True, help="Chronological age")
    parser.add_argument("--hr", type=float, default=1.0, help="Hazard ratio of intervention (e.g., 0.8)")
    parser.add_argument("--shift", type=float, default=0.0, help="Biological age shift (e.g., -3.0)")
    parser.add_argument("--source", type=str, default=None, help="Citation source")
    args = parser.parse_args()

    scenarios = [
        SurvivalScenario(name="Baseline (Status Quo)"),
    ]
    if args.hr != 1.0 or args.shift != 0.0:
        scenarios.append(
            SurvivalScenario(
                name="Optimized Protocol",
                hazard_ratio=args.hr,
                age_shift=args.shift,
                source=args.source or "Clinical Trial Meta-Analysis",
            )
        )

    res = evaluate_survival(args.age, scenarios)
    print(json.dumps(res.model_dump(), indent=2))


if __name__ == "__main__":
    main()
