from __future__ import annotations

from typing import Dict, Any, List
import math

from .science_notes import CLAIM_BOUNDARY


def validate_result(result: Dict[str, Any]) -> Dict[str, Any]:
    failures: List[str] = []
    warnings: List[str] = []

    metrics = result.get("metrics", {})
    final_total = metrics.get("final_total_population", 0)
    if not isinstance(final_total, (int, float)) or not math.isfinite(float(final_total)):
        failures.append("Final population is not finite.")
    if isinstance(final_total, (int, float)) and final_total < 0:
        failures.append("Final population is negative.")
    if not result.get("curves"):
        failures.append("No population curves were recorded.")
    if not result.get("density", {}).get("normalized"):
        failures.append("No density map was recorded.")
    if result.get("claim_boundary") != CLAIM_BOUNDARY:
        warnings.append("Claim boundary does not match current package boundary text.")
    if metrics.get("organism_count", 0) <= 0:
        failures.append("Experiment has no organisms.")
    if metrics.get("steps", 0) < 1:
        failures.append("Experiment has no steps.")

    status = "pass" if not failures else "fail"
    return {
        "status": status,
        "failures": failures,
        "warnings": warnings,
        "claim_boundary": CLAIM_BOUNDARY,
        "permitted_use": [
            "education",
            "exploratory simulation",
            "UI prototyping",
            "architecture testing",
        ],
        "not_permitted_use": [
            "clinical diagnosis",
            "drug efficacy prediction",
            "wet-lab proof",
            "patient-specific recommendation",
            "public-health forecast",
        ],
    }
