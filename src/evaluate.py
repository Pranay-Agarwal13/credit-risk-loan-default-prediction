"""
Model evaluation, performance metrics, and cost-sensitive threshold optimization.
Calculates ROC-AUC, PR-AUC, precision-recall trade-offs, and economic loss curves.
"""

import json
import os
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    roc_curve,
    confusion_matrix,
    classification_report,
    f1_score,
    precision_score,
    recall_score
)
from src.utils import logger, calculate_business_cost, DEFAULT_TIER_CUTOFFS

class ModelEvaluator:
    """Calculates held-out evaluation metrics and optimizes underwriting thresholds."""

    def __init__(self, cost_fn: float = 10000.0, cost_fp: float = 1200.0):
        self.cost_fn = cost_fn  # Default loss from approved bad borrower
        self.cost_fp = cost_fp  # Opportunity cost of declining good borrower

    def evaluate_predictions(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        threshold: float = 0.50
    ) -> Dict[str, Any]:
        """Compute full statistical evaluation at a specific threshold."""
        y_pred = (y_prob >= threshold).astype(int)

        roc_auc = float(roc_auc_score(y_true, y_prob))
        pr_auc = float(average_precision_score(y_true, y_prob))
        prec = float(precision_score(y_true, y_pred, zero_division=0))
        rec = float(recall_score(y_true, y_pred, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, zero_division=0))

        cm = confusion_matrix(y_true, y_pred).tolist()

        cost_metrics = calculate_business_cost(
            y_true=y_true,
            y_prob=y_prob,
            threshold=threshold,
            cost_fn=self.cost_fn,
            cost_fp=self.cost_fp
        )

        return {
            "threshold": threshold,
            "roc_auc": round(roc_auc, 4),
            "pr_auc": round(pr_auc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": cm,
            "cost_metrics": cost_metrics
        }

    def optimize_threshold(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        threshold_range: Tuple[float, float, float] = (0.05, 0.70, 0.01)
    ) -> Dict[str, Any]:
        """
        Sweep decision thresholds to identify:
        1. Cost-optimal threshold (minimum financial loss)
        2. F1-optimal threshold (balanced precision/recall)
        3. Recall-targeted threshold (capturing at least 70% of defaulters)
        """
        start, stop, step = threshold_range
        thresholds = np.arange(start, stop, step)

        sweep_results = []
        min_cost = float("inf")
        best_cost_threshold = 0.50
        max_f1 = -1.0
        best_f1_threshold = 0.50

        for t in thresholds:
            t = round(float(t), 3)
            y_pred = (y_prob >= t).astype(int)
            cost_res = calculate_business_cost(y_true, y_prob, t, self.cost_fn, self.cost_fp)
            
            p = float(precision_score(y_true, y_pred, zero_division=0))
            r = float(recall_score(y_true, y_pred, zero_division=0))
            f1 = float(f1_score(y_true, y_pred, zero_division=0))

            if cost_res["total_cost"] < min_cost:
                min_cost = cost_res["total_cost"]
                best_cost_threshold = t

            if f1 > max_f1:
                max_f1 = f1
                best_f1_threshold = t

            sweep_results.append({
                "threshold": t,
                "precision": round(p, 4),
                "recall": round(r, 4),
                "f1_score": round(f1, 4),
                "total_cost": cost_res["total_cost"],
                "predicted_defaults": cost_res["predicted_defaults"],
                "approval_rate": cost_res["approval_rate"]
            })

        logger.info(f"Optimal cost threshold found: {best_cost_threshold} (Min Loss: ${min_cost:,.0f})")
        logger.info(f"Max F1 threshold: {best_f1_threshold} (F1: {max_f1:.4f})")

        return {
            "best_cost_threshold": best_cost_threshold,
            "min_cost": min_cost,
            "best_f1_threshold": best_f1_threshold,
            "max_f1": max_f1,
            "sweep_table": sweep_results
        }

    def save_artifacts(
        self,
        eval_metrics: Dict[str, Any],
        threshold_config: Dict[str, Any],
        output_dir: str = "models"
    ) -> None:
        """Save metrics.json and threshold_config.json to models directory."""
        os.makedirs(output_dir, exist_ok=True)
        
        metrics_path = os.path.join(output_dir, "metrics.json")
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(eval_metrics, f, indent=2)
        logger.info(f"Saved test metrics to {metrics_path}")

        config_path = os.path.join(output_dir, "threshold_config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(threshold_config, f, indent=2)
        logger.info(f"Saved threshold configuration to {config_path}")
