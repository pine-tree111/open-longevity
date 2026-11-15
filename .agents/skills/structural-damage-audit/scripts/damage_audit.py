#!/usr/bin/env python3
"""
Structural Cellular Damage Audit Engine.

Audits longevity and clinical interventions against the 7 primary hallmarks
of structural cellular damage repair:
  1. ApoptoSENS: Senescent cell ablation / targeted clearance
  2. OncoSENS: Nuclear DNA mutation control & oncogenic interdiction
  3. MitoSENS: Mitochondrial genome rescue & allotopic repair
  4. LysoSENS: Degradation of intracellular aggregate junk (lipofuscin, 7-ketocholesterol)
  5. AmyloSENS: Clearance of extracellular protein aggregates & arterial plaque
  6. GlycoSENS: Cleavage of extracellular matrix crosslinks (glucosepane, AGEs)
  7. RepleniSENS: Stem cell replenishment & tissue regeneration for cell loss
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


DAMAGE_PILLARS = {
    "ApoptoSENS": "Senescent cell ablation / targeted clearance",
    "OncoSENS": "Nuclear mutation control / oncogenic suppression",
    "MitoSENS": "Mitochondrial repair and allotopic gene rescue",
    "LysoSENS": "Degradation of recalcitrant intracellular aggregates (lipofuscin, oxidized lipids)",
    "AmyloSENS": "Clearance of extracellular aggregates and arterial plaque substrates",
    "GlycoSENS": "Cleavage of extracellular matrix crosslinks (glucosepane, AGEs)",
    "RepleniSENS": "Stem cell replenishment and tissue regeneration for cell loss",
}

KNOWN_INTERVENTIONS: Dict[str, Dict[str, Any]] = {
    "dasatinib_quercetin": {
        "name": "Dasatinib + Quercetin (D+Q)",
        "type": "Damage Repair (Senolytic)",
        "primary_pillars": ["ApoptoSENS"],
        "mechanism": "Inhibition of BCL-2/BCL-xL/p21 survival pathways triggering apoptosis in senescent cells",
        "evidence_level": "[VERIFIED: Human Pilot RCT / Murine ITP]",
        "cadence": "Pulsed (hit-and-run, every 30-90 days)",
        "is_structural_repair": True,
    },
    "fisetin": {
        "name": "Fisetin",
        "type": "Damage Repair (Senolytic)",
        "primary_pillars": ["ApoptoSENS"],
        "mechanism": "Naturally derived flavonoid inducing apoptosis in senescent endothelial and immune cells",
        "evidence_level": "[EVIDENCED: Murine ITP / Ongoing Human Trials]",
        "cadence": "Pulsed administration",
        "is_structural_repair": True,
    },
    "rapamycin": {
        "name": "Rapamycin (Sirolimus)",
        "type": "Metabolic Modulator / Autophagy Enhancer",
        "primary_pillars": ["LysoSENS"],
        "mechanism": "mTORC1 inhibition, stimulating macroautophagy and lysosomal degradation of damaged organelles",
        "evidence_level": "[VERIFIED: Murine ITP (Gold Standard) / Observational Human]",
        "cadence": "Weekly pulsed oral dosing",
        "is_structural_repair": False,  # Metabolic signaling tuning
    },
    "rosuvastatin_ezetimibe": {
        "name": "Rosuvastatin + Ezetimibe",
        "type": "Damage Prevention & Plaque Substrate Clearance",
        "primary_pillars": ["AmyloSENS", "GlycoSENS"],
        "mechanism": "HMG-CoA reductase + NPC1L1 dual inhibition; clears circulating ApoB particles before vascular oxidation and atheroma deposition",
        "evidence_level": "[VERIFIED: Human Large-Scale RCTs (IMPROVE-IT, JUPITER)]",
        "cadence": "Daily oral administration",
        "is_structural_repair": True,
    },
    "metformin": {
        "name": "Metformin",
        "type": "Metabolic Modulator",
        "primary_pillars": [],
        "mechanism": "Mild mitochondrial Complex I inhibition, AMPK activation, reduction of hepatic gluconeogenesis",
        "evidence_level": "[VERIFIED: Human T2D Cohorts]",
        "cadence": "Daily oral administration",
        "is_structural_repair": False,
    },
}


class InterventionAudit(BaseModel):
    name: str
    type: str
    primary_pillars: List[str]
    mechanism: str
    evidence_level: str
    cadence: str
    is_structural_repair: bool


def audit_intervention(key: str) -> Optional[InterventionAudit]:
    norm_key = key.lower().replace("-", "_").replace(" ", "_")
    data = KNOWN_INTERVENTIONS.get(norm_key)
    if not data:
        return None
    return InterventionAudit(**data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Structural Cellular Damage Audit Engine")
    parser.add_argument("--intervention", type=str, required=True, help="Intervention key (e.g. dasatinib_quercetin, rapamycin)")
    args = parser.parse_args()

    audit = audit_intervention(args.intervention)
    if not audit:
        print(f"Error: Intervention '{args.intervention}' not found in known database.")
        print(f"Available: {', '.join(KNOWN_INTERVENTIONS.keys())}")
        return

    print(json.dumps(audit.model_dump(), indent=2))


if __name__ == "__main__":
    main()
