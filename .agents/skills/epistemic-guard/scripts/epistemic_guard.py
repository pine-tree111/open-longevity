#!/usr/bin/env python3
"""
Epistemic Guard & Anti-Hype Refusal Engine.

Adapted from the open-source PLSI architecture (https://github.com/Insilico-org/plsi)
under the MIT License.

Enforces strict scientific integrity standards:
1. Mandatory Falsifiers: Biological hypotheses must provide an explicit 'if_false' refutation condition.
2. Anti-Hype Filter: Superlative claims ('first-in-class', 'the only', 'proven cure')
   are refused unless anchored by a verified citation identifier (PMID, NCT, DOI) in the same sentence.
3. Vague Biohacking Refusal: Rejects subjective wellness filler lacking measurable biomarker endpoints.
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Any, List, Optional
from pydantic import BaseModel, Field


SUPERLATIVE_PATTERNS = [
    r"\bthe\s+(?:only|sole|first|best|leading|strongest|largest|lone|single|most\b\s*\w*)",
    r"\b(?:nobody|no\s?one|none)\b",
    r"\bno\s+(?:other|further|competing|competitor|company|sponsor|clinical|published|identified|known|approved|disclosed|existing|rival|drug|asset|molecule|programme|trial)\w*",
    r"\bfirst[-\s]in[-\s]class\b",
    r"\bunprecedented\b",
    r"\bnever\s+been\b",
    r"\bproven\s+(?:cure|fix|breakthrough|solution)\b",
    r"\bcompletely\s+reverses?\b",
    r"\bguaranteed\b",
    r"\bzero\s+risk\b",
    r"\bmiracle\b",
]

CITATION_PATTERNS = [
    r"PMID[:\s]*\d{1,9}",
    r"NCT[:\s]*\d{8}",
    r"\b10\.\d{4,9}/\S+",
    r"doi[:\s]*10\.\S+",
    r"CHEMBL[:\s]*\d+",
    r"ENSG[:\s]*\d{11}",
    r"PDB[:\s]*\d[A-Za-z0-9]{3}",
]

VAGUE_BIOHACK_PATTERNS = [
    r"\bfelt\s+(?:more\s+energetic|amazing|cleansed|rejuvenated|lighter)\b",
    r"\bdetox(?:ifies|ification|ed)?\b",
    r"\bboosts?\s+(?:vitality|vibrations|natural\s+energy)\b",
    r"\bflushes?\s+out\s+toxins\b",
]

SUPERLATIVE_REGEX = re.compile("|".join(SUPERLATIVE_PATTERNS), re.IGNORECASE)
CITATION_REGEX = re.compile("|".join(CITATION_PATTERNS), re.IGNORECASE)
VAGUE_REGEX = re.compile("|".join(VAGUE_BIOHACK_PATTERNS), re.IGNORECASE)


class EpistemicViolation(BaseModel):
    refusal_code: str
    category: str
    message: str
    violating_snippet: str
    remedy: str


class AuditReport(BaseModel):
    passed: bool
    violations: List[EpistemicViolation]


def audit_hypothesis(hypothesis: str, if_false: Optional[str]) -> List[EpistemicViolation]:
    """Ensure hypothesis has a falsifiable test condition."""
    violations: List[EpistemicViolation] = []
    if not if_false or not str(if_false).strip():
        violations.append(
            EpistemicViolation(
                refusal_code="REFUSAL-UNFALSIFIABLE",
                category="Unfalsifiable Hypothesis",
                message="Hypothesis lacks an explicit 'if_false' refutation condition.",
                violating_snippet=hypothesis[:120],
                remedy="State explicitly what empirical observation would prove this hypothesis wrong.",
            )
        )
    return violations


def audit_text_integrity(text: str) -> List[EpistemicViolation]:
    """Audit prose for superlatives without citations and vague biohacking."""
    violations: List[EpistemicViolation] = []

    sentences = re.split(r"(?<=[.!?])\s+", text)
    for sent in sentences:
        s_clean = sent.strip()
        if not s_clean:
            continue

        # Check superlatives without in-sentence citation
        if SUPERLATIVE_REGEX.search(s_clean):
            if not CITATION_REGEX.search(s_clean):
                match = SUPERLATIVE_REGEX.search(s_clean)
                matched_word = match.group(0) if match else "superlative"
                violations.append(
                    EpistemicViolation(
                        refusal_code="REFUSAL-SUPERLATIVE",
                        category="Unanchored Superlative",
                        message=f"Sentence contains absolute/superlative claim ('{matched_word}') without a verified citation.",
                        violating_snippet=s_clean[:140],
                        remedy="Cite a verified identifier (PMID, NCT, DOI) in the same sentence or remove the superlative.",
                    )
                )

        # Check vague unquantified biohacking
        vague_match = VAGUE_REGEX.search(s_clean)
        if vague_match:
            violations.append(
                EpistemicViolation(
                    refusal_code="REFUSAL-VAGUE",
                    category="Unquantified Biohacking",
                    message=f"Sentence uses unquantified subjective wellness language ('{vague_match.group(0)}').",
                    violating_snippet=s_clean[:140],
                    remedy="Replace subjective feeling with objective biomarker endpoints (e.g. hs-CRP, ApoB, VO2 max).",
                )
            )

    return violations


def audit_protocol(protocol_text: str, hypotheses: Optional[List[dict[str, str]]] = None) -> AuditReport:
    """Run full epistemic audit on text and structured hypotheses."""
    violations: List[EpistemicViolation] = []
    violations.extend(audit_text_integrity(protocol_text))

    if hypotheses:
        for h in hypotheses:
            violations.extend(audit_hypothesis(h.get("hypothesis", ""), h.get("if_false")))

    return AuditReport(passed=len(violations) == 0, violations=violations)


def main() -> None:
    parser = argparse.ArgumentParser(description="Epistemic Guard & Anti-Hype Refusal Auditor.")
    parser.add_argument("--text", type=str, required=True, help="Text to audit")
    args = parser.parse_args()

    report = audit_protocol(args.text)
    print(json.dumps(report.model_dump(), indent=2))


if __name__ == "__main__":
    main()
