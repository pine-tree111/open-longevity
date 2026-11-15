#!/usr/bin/env python3
"""
Open-Longevity Autonomous Biomarker Triage Engine.

Algorithmic, evidence-based triage scoring of baseline blood biomarkers against
consensus cardiology, endocrinology, and longevity medicine guidelines.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TriageResult(BaseModel):
    category: str
    marker: str
    value: float
    unit: str
    status: str  # OPTIMAL, SUBOPTIMAL, CRITICAL
    reference_target: str
    finding: str
    action_directive: str


class BiomarkerTriageEvaluator:
    def __init__(self) -> None:
        pass

    def evaluate_lipids(self, lipids: Dict[str, Optional[float]]) -> List[TriageResult]:
        results: List[TriageResult] = []
        
        # ApoB
        apob = lipids.get("apob_mg_dl")
        if apob is not None:
            if apob < 60:
                status, target, finding, action = (
                    "OPTIMAL", "< 60 mg/dL", "Superior arterial plaque protection", "Maintain current baseline"
                )
            elif apob <= 90:
                status, target, finding, action = (
                    "SUBOPTIMAL", "< 60 mg/dL", "Mild atherogenic particle elevation", "Evaluate dietary saturated fat & fiber intake"
                )
            else:
                status, target, finding, action = (
                    "CRITICAL", "< 60 mg/dL", "High atherogenic particle concentration; active plaque progression risk",
                    "Consult physician for aggressive lipid-lowering evaluation (e.g., statin/ezetimibe therapy)"
                )
            results.append(TriageResult(category="Lipids", marker="ApoB", value=apob, unit="mg/dL", status=status, reference_target=target, finding=finding, action_directive=action))

        # LDL-C
        ldl = lipids.get("ldl_c_mg_dl")
        if ldl is not None:
            if ldl < 70:
                status, target, finding, action = (
                    "OPTIMAL", "< 70 mg/dL", "Low atherogenic circulating burden", "Maintain current baseline"
                )
            elif ldl <= 100:
                status, target, finding, action = (
                    "SUBOPTIMAL", "< 70 mg/dL", "Moderate atherogenic burden", "Increase soluble fiber and review dietary saturated fat"
                )
            elif ldl < 190:
                status, target, finding, action = (
                    "CRITICAL", "< 70 mg/dL", "Elevated LDL-C driving endothelial particle deposition", "Discuss lipid-lowering intervention with physician"
                )
            else:
                status, target, finding, action = (
                    "CRITICAL", "< 70 mg/dL", "Severe hypercholesterolemia (suspected familial dyslipidemia)", "Urgent clinical cardiovascular evaluation required"
                )
            results.append(TriageResult(category="Lipids", marker="LDL-C", value=ldl, unit="mg/dL", status=status, reference_target=target, finding=finding, action_directive=action))

        # Triglycerides / HDL ratio
        trig = lipids.get("triglycerides_mg_dl")
        hdl = lipids.get("hdl_c_mg_dl")
        if trig is not None and hdl is not None and hdl > 0:
            ratio = round(trig / hdl, 2)
            if ratio < 1.5:
                status, target, finding, action = ("OPTIMAL", "< 1.5", "High insulin sensitivity", "Maintain routine")
            elif ratio <= 3.0:
                status, target, finding, action = ("SUBOPTIMAL", "< 1.5", "Early metabolic resistance pattern", "Reduce refined starches, add post-meal walks")
            else:
                status, target, finding, action = ("CRITICAL", "< 1.5", "Significant insulin resistance & atherogenic dyslipidemia", "Mandatory dietary restructuring and metabolic screening")
            results.append(TriageResult(category="Lipids", marker="Trig/HDL Ratio", value=ratio, unit="ratio", status=status, reference_target=target, finding=finding, action_directive=action))

        return results

    def evaluate_glycemic(self, glycemic: Dict[str, Optional[float]]) -> List[TriageResult]:
        results: List[TriageResult] = []

        # Fasting Glucose
        fpg = glycemic.get("fasting_glucose_mg_dl")
        if fpg is not None:
            if fpg < 90:
                status, target, finding, action = ("OPTIMAL", "70-89 mg/dL", "Optimal hepatic glucose suppression", "Maintain current nutritional pattern")
            elif fpg < 100:
                status, target, finding, action = ("SUBOPTIMAL", "70-89 mg/dL", "High-normal fasting glucose", "Audit evening carbohydrate timing")
            elif fpg < 126:
                status, target, finding, action = ("CRITICAL", "70-89 mg/dL", "Impaired Fasting Glucose (Prediabetes)", "Adopt zero liquid sugar, post-meal walks, and physician review")
            else:
                status, target, finding, action = ("CRITICAL", "70-89 mg/dL", "Diabetic range fasting hyperglycemia", "Immediate physician evaluation for metabolic therapy")
            results.append(TriageResult(category="Metabolic", marker="Fasting Glucose", value=fpg, unit="mg/dL", status=status, reference_target=target, finding=finding, action_directive=action))

        # HbA1c
        a1c = glycemic.get("hba1c_percent")
        if a1c is not None:
            if a1c < 5.4:
                status, target, finding, action = ("OPTIMAL", "< 5.4%", "Minimal non-enzymatic protein glycation", "Maintain current dietary fiber and exercise")
            elif a1c <= 5.6:
                status, target, finding, action = ("SUBOPTIMAL", "< 5.4%", "Normal, but mild cumulative glycation", "Optimize postprandial exercise kinetics")
            elif a1c <= 6.4:
                status, target, finding, action = ("CRITICAL", "< 5.4%", "Prediabetes range cumulative glycation", "Structured carbohydrate elimination and insulin sensitivity protocol")
            else:
                status, target, finding, action = ("CRITICAL", "< 5.4%", "Diabetic glycation burden", "Urgent clinical endocrine management")
            results.append(TriageResult(category="Metabolic", marker="HbA1c", value=a1c, unit="%", status=status, reference_target=target, finding=finding, action_directive=action))

        # 2-Hr OGTT
        ogtt = glycemic.get("two_hour_ogtt_mg_dl")
        if ogtt is not None:
            if ogtt < 120:
                status, target, finding, action = ("OPTIMAL", "< 120 mg/dL", "Robust peripheral glucose disposal", "Maintain routine")
            elif ogtt < 140:
                status, target, finding, action = ("SUBOPTIMAL", "< 120 mg/dL", "Normal glucose tolerance with delayed return", "Increase resistance training and muscle GLUT4 mass")
            elif ogtt < 200:
                status, target, finding, action = ("CRITICAL", "< 120 mg/dL", "Impaired Glucose Tolerance (Severe IGT)", "Mandatory post-meal walking (15 min), eliminate white flour/sugar, physician review")
            else:
                status, target, finding, action = ("CRITICAL", "< 120 mg/dL", "Diabetic glucose tolerance response", "Immediate clinical medical management")
            results.append(TriageResult(category="Metabolic", marker="2-Hr OGTT", value=ogtt, unit="mg/dL", status=status, reference_target=target, finding=finding, action_directive=action))

        return results

    def evaluate_inflammation_and_organs(self, cv: Dict[str, Optional[float]], organs: Dict[str, Optional[float]]) -> List[TriageResult]:
        results: List[TriageResult] = []

        # hs-CRP
        crp = cv.get("hs_crp_mg_l")
        if crp is not None:
            if crp < 0.5:
                status, target, finding, action = ("OPTIMAL", "< 0.5 mg/L", "Negligible systemic vascular inflammation", "Maintain anti-inflammatory lifestyle")
            elif crp <= 1.0:
                status, target, finding, action = ("SUBOPTIMAL", "< 0.5 mg/L", "Low-grade background inflammatory activity", "Audit sleep quality, dental hygiene, and visceral fat")
            elif crp <= 3.0:
                status, target, finding, action = ("CRITICAL", "< 0.5 mg/L", "Moderate systemic inflammation; independent cardiovascular risk multiplier", "Investigate chronic infection, metabolic syndrome, or dental pathology")
            else:
                status, target, finding, action = ("CRITICAL", "< 0.5 mg/L", "High active inflammation", "Medical evaluation to rule out acute infection or autoimmune flare")
            results.append(TriageResult(category="Inflammation", marker="hs-CRP", value=crp, unit="mg/L", status=status, reference_target=target, finding=finding, action_directive=action))

        # ALT
        alt = organs.get("alt_u_l")
        if alt is not None:
            if alt <= 25:
                status, target, finding, action = ("OPTIMAL", "10-25 U/L", "Optimal hepatic safety and zero transaminase leak", "Maintain baseline")
            elif alt <= 40:
                status, target, finding, action = ("SUBOPTIMAL", "10-25 U/L", "Mildly elevated hepatocellular stress", "Screen for hepatic steatosis (liver fat), reduce alcohol/fructose")
            else:
                status, target, finding, action = ("CRITICAL", "10-25 U/L", "Significant transaminase elevation (potential steatohepatitis)", "Physician consultation, abdominal ultrasound, metabolic review")
            results.append(TriageResult(category="Hepatic", marker="ALT", value=alt, unit="U/L", status=status, reference_target=target, finding=finding, action_directive=action))

        return results


def run_triage(data: Dict[str, Any]) -> Dict[str, Any]:
    evaluator = BiomarkerTriageEvaluator()
    biomarkers = data.get("baseline_biomarkers", {})
    
    findings: List[TriageResult] = []
    findings.extend(evaluator.evaluate_lipids(biomarkers.get("lipids", {})))
    findings.extend(evaluator.evaluate_glycemic(biomarkers.get("glycemic_and_metabolic", {})))
    findings.extend(evaluator.evaluate_inflammation_and_organs(
        biomarkers.get("cardiovascular_and_inflammatory", {}),
        biomarkers.get("organ_safety_and_renal", {})
    ))

    optimal = [f.model_dump() for f in findings if f.status == "OPTIMAL"]
    suboptimal = [f.model_dump() for f in findings if f.status == "SUBOPTIMAL"]
    critical = [f.model_dump() for f in findings if f.status == "CRITICAL"]

    return {
        "summary": {
            "total_markers_analyzed": len(findings),
            "optimal_count": len(optimal),
            "suboptimal_count": len(suboptimal),
            "critical_kill_vectors_count": len(critical),
        },
        "critical_kill_vectors": critical,
        "suboptimal_opportunities": suboptimal,
        "optimal_markers": optimal,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Open-Longevity Biomarker Triage Engine")
    parser.add_argument("--profile", type=str, default="profile/user_profile.yaml", help="Path to user_profile.yaml")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    profile_path = Path(args.profile)
    if not profile_path.exists():
        fallback = Path("profile/user_profile.template.yaml")
        if fallback.exists():
            profile_path = fallback
        else:
            print(f"Error: Profile not found at {args.profile}")
            return

    import yaml
    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    report = run_triage(data)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("\n=== OPEN-LONGEVITY BIOMARKER TRIAGE REPORT ===")
        print(f"Analyzed: {report['summary']['total_markers_analyzed']} markers")
        print(f"Optimal: {report['summary']['optimal_count']} | Suboptimal: {report['summary']['suboptimal_count']} | Critical: {report['summary']['critical_kill_vectors_count']}\n")
        
        if report["critical_kill_vectors"]:
            print("🚨 CRITICAL KILL-VECTORS DETECTED:")
            for item in report["critical_kill_vectors"]:
                print(f"  [{item['category']}] {item['marker']}: {item['value']} {item['unit']} (Target: {item['reference_target']})")
                print(f"    Finding: {item['finding']}")
                print(f"    Action:  {item['action_directive']}\n")

        if report["suboptimal_opportunities"]:
            print("⚠️ SUBOPTIMAL LIFESTYLE OPPORTUNITIES:")
            for item in report["suboptimal_opportunities"]:
                print(f"  [{item['category']}] {item['marker']}: {item['value']} {item['unit']} (Target: {item['reference_target']})")
                print(f"    Action:  {item['action_directive']}\n")

        if report["optimal_markers"]:
            print("✅ OPTIMAL BASELINES:")
            for item in report["optimal_markers"]:
                print(f"  [{item['category']}] {item['marker']}: {item['value']} {item['unit']} - {item['finding']}")
        print("==============================================\n")


if __name__ == "__main__":
    main()
