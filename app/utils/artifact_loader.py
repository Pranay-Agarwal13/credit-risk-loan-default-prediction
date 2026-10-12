"""
Artifact loader for Streamlit application.
Loads models, metadata, thresholds, metrics, and SHAP objects with @st.cache_resource.
Provides friendly setup instructions if files are missing.
"""

import os
import json
from typing import Dict, Any, Optional, Tuple
import pandas as pd
import joblib
import streamlit as st

@st.cache_resource(show_spinner=False)
def load_feature_metadata(models_dir: str = "models") -> Optional[Dict[str, Any]]:
    """Load feature metadata schema with caching."""
    path = os.path.join(models_dir, "feature_metadata.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@st.cache_resource(show_spinner=False)
def load_threshold_config(models_dir: str = "models") -> Dict[str, Any]:
    """Load threshold configuration and risk tier cutoffs."""
    path = os.path.join(models_dir, "threshold_config.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Default fallback configuration
    return {
        "selected_threshold": 0.24,
        "default_threshold": 0.50,
        "cost_assumptions": {"false_negative_cost": 10000.0, "false_positive_cost": 1200.0},
        "risk_tier_cutoffs": {"low": 0.10, "medium": 0.25, "high": 0.50, "critical": 1.00},
        "actions_by_tier": {
            "Low": "Instant Approval - Prime Interest Rates",
            "Medium": "Approved with Standard Automated Verification Check",
            "High": "Escalate to Senior Underwriter for Manual Committee Review",
            "Critical": "Adverse Decision / Automated Decline or Secured Exception Only"
        }
    }

@st.cache_resource(show_spinner=False)
def load_metrics(models_dir: str = "models") -> Optional[Dict[str, Any]]:
    """Load held-out test evaluation metrics."""
    path = os.path.join(models_dir, "metrics.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@st.cache_resource(show_spinner=False)
def load_segment_insights(models_dir: str = "models") -> Optional[pd.DataFrame]:
    """Load DuckDB SQL business segment insights."""
    path = os.path.join(models_dir, "segment_insights.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_resource(show_spinner=False)
def load_model_pipeline(models_dir: str = "models") -> Optional[Any]:
    """Load serialized scikit-learn model pipeline."""
    path = os.path.join(models_dir, "model_pipeline.joblib")
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception as e:
            return None
    return None

@st.cache_resource(show_spinner=False)
def load_shap_explainer(models_dir: str = "models") -> Optional[Any]:
    """Load pre-fitted TreeSHAP explainer object."""
    path = os.path.join(models_dir, "shap_explainer.joblib")
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception:
            return None
    return None

def render_missing_artifact_warning(missing_items: list, models_dir: str = "models"):
    """Render helpful actionable instructions when artifacts are missing."""
    st.warning(
        f"**Missing Model Artifacts Detected in `{models_dir}/`**:\n"
        + "".join([f"- `{item}`\n" for item in missing_items])
        + "\n**How to generate production artifacts**:\n"
        + "1. Ensure `data/raw/application_train.csv` is present (or use synthetic generator).\n"
        + "2. Run training in your terminal: `python src/train.py`\n"
        + "The app will automatically cache and display live trained outputs once available."
    )
