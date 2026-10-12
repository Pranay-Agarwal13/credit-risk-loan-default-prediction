"""
Mock data generator for AI Studio interactive UI preview.
Generates representative portfolio applicants across all four risk tiers:
Low, Medium, High, and Critical.
Dependency-free standard library implementation.
"""

from typing import List, Dict, Any

def get_mock_portfolio_applicants(n: int = 15) -> List[Dict[str, Any]]:
    """Return realistic mock applicant profiles spanning all risk tiers."""
    applicants = [
        {
            "id": "APP-2001",
            "name": "Sarah Jenkins",
            "income": 240000,
            "credit": 450000,
            "annuity": 22500,
            "dti": 1.88,
            "ext_score": 0.78,
            "bureau_active": 1,
            "bureau_debt": 42000,
            "age": 45,
            "employed_years": 11.5,
            "probability": 0.034,
            "tier": "Low",
            "action": "Instant Approval - Prime Interest Rates",
            "decision": "PASS (ACCEPT)"
        },
        {
            "id": "APP-2002",
            "name": "Thomas Sterling",
            "income": 195000,
            "credit": 480000,
            "annuity": 24000,
            "dti": 2.46,
            "ext_score": 0.72,
            "bureau_active": 1,
            "bureau_debt": 38000,
            "age": 42,
            "employed_years": 8.0,
            "probability": 0.052,
            "tier": "Low",
            "action": "Instant Approval - Prime Interest Rates",
            "decision": "PASS (ACCEPT)"
        },
        {
            "id": "APP-2003",
            "name": "David Ramirez",
            "income": 135000,
            "credit": 520000,
            "annuity": 28400,
            "dti": 3.85,
            "ext_score": 0.49,
            "bureau_active": 2,
            "bureau_debt": 165000,
            "age": 36,
            "employed_years": 4.9,
            "probability": 0.142,
            "tier": "Medium",
            "action": "Approved with Standard Automated Verification Check",
            "decision": "PASS (ACCEPT)"
        },
        {
            "id": "APP-2004",
            "name": "Rachel Kim",
            "income": 120000,
            "credit": 490000,
            "annuity": 27200,
            "dti": 4.08,
            "ext_score": 0.46,
            "bureau_active": 2,
            "bureau_debt": 180000,
            "age": 33,
            "employed_years": 3.2,
            "probability": 0.186,
            "tier": "Medium",
            "action": "Approved with Standard Automated Verification Check",
            "decision": "PASS (ACCEPT)"
        },
        {
            "id": "APP-2005",
            "name": "Marcus Vance",
            "income": 90000,
            "credit": 640000,
            "annuity": 39500,
            "dti": 7.11,
            "ext_score": 0.27,
            "bureau_active": 4,
            "bureau_debt": 490000,
            "age": 27,
            "employed_years": 1.2,
            "probability": 0.384,
            "tier": "High",
            "action": "Escalate to Senior Underwriter for Manual Committee Review",
            "decision": "FLAGGED FOR REVIEW / DECLINE"
        },
        {
            "id": "APP-2006",
            "name": "Carlos Gomez",
            "income": 82000,
            "credit": 580000,
            "annuity": 36200,
            "dti": 7.07,
            "ext_score": 0.29,
            "bureau_active": 3,
            "bureau_debt": 410000,
            "age": 29,
            "employed_years": 1.5,
            "probability": 0.352,
            "tier": "High",
            "action": "Escalate to Senior Underwriter for Manual Committee Review",
            "decision": "FLAGGED FOR REVIEW / DECLINE"
        },
        {
            "id": "APP-2007",
            "name": "Elena Rostova",
            "income": 65000,
            "credit": 550000,
            "annuity": 36800,
            "dti": 8.46,
            "ext_score": 0.12,
            "bureau_active": 5,
            "bureau_debt": 460000,
            "age": 23,
            "employed_years": 0.5,
            "probability": 0.682,
            "tier": "Critical",
            "action": "Adverse Decision / Automated Decline or Secured Exception Only",
            "decision": "FLAGGED FOR REVIEW / DECLINE"
        },
        {
            "id": "APP-2008",
            "name": "Julian Bell",
            "income": 58000,
            "credit": 490000,
            "annuity": 34100,
            "dti": 8.45,
            "ext_score": 0.10,
            "bureau_active": 4,
            "bureau_debt": 420000,
            "age": 22,
            "employed_years": 0.3,
            "probability": 0.724,
            "tier": "Critical",
            "action": "Adverse Decision / Automated Decline or Secured Exception Only",
            "decision": "FLAGGED FOR REVIEW / DECLINE"
        }
    ]
    return applicants[:n]

def get_mock_shap_breakdown(probability: float, dti: float, ext_score: float) -> Dict[str, Any]:
    """Generate dynamic mock SHAP attribution based on input factors."""
    drivers = []
    mitigators = []

    # DTI impact
    if dti > 4.0:
        drivers.append({"display_name": "High Debt-to-Income Leverage", "feature_value": dti, "shap_value": round((dti - 3.5) * 0.12, 2)})
    else:
        mitigators.append({"display_name": "Conservative Debt Leverage", "feature_value": dti, "shap_value": round((dti - 3.5) * 0.10, 2)})

    # External score impact
    if ext_score < 0.40:
        drivers.append({"display_name": "Adverse External Bureau Score", "feature_value": ext_score, "shap_value": round((0.45 - ext_score) * 0.85, 2)})
    else:
        mitigators.append({"display_name": "Strong External Credit Rating", "feature_value": ext_score, "shap_value": round((0.45 - ext_score) * 0.85, 2)})

    return {
        "base_value": 0.0807,
        "top_drivers": sorted(drivers, key=lambda x: x["shap_value"], reverse=True),
        "top_mitigators": sorted(mitigators, key=lambda x: x["shap_value"]),
        "disclaimer": "SHAP feature attributions identify statistical associations learned by the model from historical correlations and do not represent proven causal relationships."
    }
