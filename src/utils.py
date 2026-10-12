"""
Utilities and helper functions for Credit Risk & Loan Default Prediction.
Includes cost-loss calculations, risk-tier binning, reproducibility seeds, and formatting.
"""

import os
import json
import random
import logging
from typing import Dict, Any, Tuple
import numpy as np

# Configure standard logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("CreditRiskSystem")

DEFAULT_SEED = 42

def set_seed(seed: int = DEFAULT_SEED) -> None:
    """Set global random seeds for deterministic execution."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    logger.info(f"Global random seed locked to {seed}")

# Default Risk Tier Cutoffs and Decision Matrix
DEFAULT_TIER_CUTOFFS = {
    "low": 0.10,        # [0.00, 0.10)
    "medium": 0.25,     # [0.10, 0.25)
    "high": 0.50,       # [0.25, 0.50)
    "critical": 1.00    # [0.50, 1.00]
}

def assign_risk_tier(probability: float, cutoffs: Dict[str, float] = None) -> Tuple[str, str, str]:
    """
    Map default probability to standard credit underwriting risk tier,
    recommended action, and badge color token.
    
    Returns:
        Tuple of (tier_name, recommended_action, color_status)
    """
    if cutoffs is None:
        cutoffs = DEFAULT_TIER_CUTOFFS

    if probability < cutoffs["low"]:
        return (
            "Low",
            "Instant Approval - Standard Prime Terms",
            "emerald"
        )
    elif probability < cutoffs["medium"]:
        return (
            "Medium",
            "Approved with Automated Verification Check",
            "amber"
        )
    elif probability < cutoffs["high"]:
        return (
            "High",
            "Refer to Senior Credit Underwriter / Committee",
            "orange"
        )
    else:
        return (
            "Critical",
            "Adverse Decision / Decline or Secured Exception Only",
            "crimson"
        )

def calculate_business_cost(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
    cost_fn: float = 10000.0,
    cost_fp: float = 1200.0,
    profit_tp: float = 0.0,
    profit_tn: float = 3500.0
) -> Dict[str, float]:
    """
    Calculate financial cost/loss of credit decisions under a given probability threshold.
    
    Business assumptions:
    - False Negative (FN): Approved a loan that defaulted. High loss (e.g. $10,000 average charge-off).
    - False Positive (FP): Declined a good borrower. Opportunity loss of interest (e.g. $1,200).
    - True Negative (TN): Correctly approved good borrower. Earns interest margin (e.g. $3,500).
    - True Positive (TP): Correctly declined risky borrower. Prevents default loss.
    """
    y_pred = (y_prob >= threshold).astype(int)
    
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    
    total_cost = (fn * cost_fn) + (fp * cost_fp)
    net_economic_value = (tn * profit_tn) - total_cost
    
    return {
        "threshold": float(threshold),
        "total_cost": float(total_cost),
        "net_economic_value": float(net_economic_value),
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "predicted_defaults": int(tp + fp),
        "approval_rate": float((tn + fn) / max(1, len(y_true))),
        "default_catch_rate": float(tp / max(1, tp + fn))
    }

def format_currency(val: float) -> str:
    """Format floating point numbers into currency strings."""
    if val is None or np.isnan(val):
        return "N/A"
    return f"${val:,.0f}"

def format_pct(val: float) -> str:
    """Format ratio into clean percentage string."""
    if val is None or np.isnan(val):
        return "N/A"
    return f"{val * 100:.1f}%"
