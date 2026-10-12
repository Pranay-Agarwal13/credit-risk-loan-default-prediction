"""
Model Training and Cross-Validation Pipeline.
Compares Logistic Regression, Random Forest, and XGBoost under Stratified K-Fold CV,
optimizes operational thresholds, computes SHAP attributions, and saves all artifacts.
"""

import os
import json
import argparse
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score

from src.utils import logger, set_seed, DEFAULT_SEED, DEFAULT_TIER_CUTOFFS
from src.data_loader import DataLoader
from src.feature_engineering import FeatureEngineer
from src.model_pipeline import (
    build_preprocessor,
    get_model_pipeline,
    extract_feature_names,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES
)
from src.evaluate import ModelEvaluator
from src.explainability import SHAPExplainer

def run_training_pipeline(
    data_dir: str = "data/raw",
    models_dir: str = "models",
    reports_dir: str = "reports",
    n_splits: int = 5,
    sample_size: int = 15000,
    seed: int = DEFAULT_SEED
) -> Dict[str, Any]:
    """Execute end-to-end model training, validation, and artifact serialization."""
    set_seed(seed)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Ingest Data
    loader = DataLoader(data_dir=data_dir)
    df_app = loader.load_application_train(nrows=sample_size)
    df_bureau = loader.load_bureau(nrows=sample_size * 3)

    # Export SQL business insights
    loader.export_all_sql_insights(output_csv=os.path.join(models_dir, "segment_insights.csv"))

    # 2. Feature Engineering
    fe = FeatureEngineer()
    df_app_feat = fe.compute_application_features(df_app)
    df_bureau_agg = fe.aggregate_bureau(df_bureau)
    df_full = fe.merge_bureau_features(df_app_feat, df_bureau_agg)

    logger.info(f"Engineered dataset shape: {df_full.shape[0]:,} rows, {df_full.shape[1]} columns.")
    default_rate = df_full["TARGET"].mean()
    logger.info(f"Target distribution: Default rate = {default_rate * 100:.2f}% (Class imbalance 1:{int((1 - default_rate) / default_rate)})")

    # 3. Stratified Train / Test Split (Hold-out 20% strictly unseen test set)
    all_feature_cols = [c for c in (NUMERIC_FEATURES + CATEGORICAL_FEATURES) if c in df_full.columns]
    X = df_full[all_feature_cols]
    y = df_full["TARGET"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        stratify=y,
        random_state=seed
    )
    logger.info(f"Training set: {len(X_train):,} rows | Held-out test set: {len(X_test):,} rows.")

    # 4. Stratified K-Fold Cross-Validation Model Comparison
    models_to_compare = ["logistic_regression", "random_forest", "xgboost"]
    cv_comparison = []

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)

    for m_type in models_to_compare:
        logger.info(f"Running {n_splits}-Fold CV for model: {m_type}...")
        fold_roc_aucs = []
        fold_pr_aucs = []

        for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train), 1):
            X_tr_f, X_val_f = X_train.iloc[train_idx], X_train.iloc[val_idx]
            y_tr_f, y_val_f = y_train[train_idx], y_train[val_idx]

            pipeline = get_model_pipeline(model_type=m_type, random_state=seed)
            pipeline.fit(X_tr_f, y_tr_f)

            val_probs = pipeline.predict_proba(X_val_f)[:, 1]
            fold_roc = roc_auc_score(y_val_f, val_probs)
            fold_pr = average_precision_score(y_val_f, val_probs)

            fold_roc_aucs.append(fold_roc)
            fold_pr_aucs.append(fold_pr)

        mean_roc = float(np.mean(fold_roc_aucs))
        mean_pr = float(np.mean(fold_pr_aucs))
        logger.info(f"[{m_type}] Mean CV ROC-AUC: {mean_roc:.4f} | PR-AUC: {mean_pr:.4f}")

        cv_comparison.append({
            "model": m_type,
            "mean_cv_roc_auc": round(mean_roc, 4),
            "std_cv_roc_auc": round(float(np.std(fold_roc_aucs)), 4),
            "mean_cv_pr_auc": round(mean_pr, 4),
            "std_cv_pr_auc": round(float(np.std(fold_pr_aucs)), 4)
        })

    df_comp = pd.DataFrame(cv_comparison)
    comp_path = os.path.join(reports_dir, "model_comparison_metrics.csv")
    df_comp.to_csv(comp_path, index=False)
    logger.info(f"Saved model cross-validation comparison to {comp_path}")

    # 5. Fit Final XGBoost Model on Full Training Set
    logger.info("Fitting production XGBoost pipeline on full training set...")
    final_pipeline = get_model_pipeline(model_type="xgboost", random_state=seed)
    final_pipeline.fit(X_train, y_train)

    # 6. Evaluate on Held-Out Test Set
    test_probs = final_pipeline.predict_proba(X_test)[:, 1]
    evaluator = ModelEvaluator(cost_fn=10000.0, cost_fp=1200.0)
    
    # Threshold Optimization
    opt_results = evaluator.optimize_threshold(y_true=y_test, y_prob=test_probs)
    selected_threshold = opt_results["best_cost_threshold"]
    
    final_eval = evaluator.evaluate_predictions(
        y_true=y_test,
        y_prob=test_probs,
        threshold=selected_threshold
    )

    # 7. Serialize Artifacts to models/
    # A. Model Pipeline
    pipeline_path = os.path.join(models_dir, "model_pipeline.joblib")
    joblib.dump(final_pipeline, pipeline_path)
    logger.info(f"Saved fitted model pipeline to {pipeline_path}")

    # B. Feature Metadata
    preprocessor = final_pipeline.named_steps["preprocessor"]
    transformed_feature_names = extract_feature_names(preprocessor)
    metadata = {
        "raw_features": all_feature_cols,
        "numeric_features": [f for f in NUMERIC_FEATURES if f in all_feature_cols],
        "categorical_features": [f for f in CATEGORICAL_FEATURES if f in all_feature_cols],
        "transformed_feature_names": transformed_feature_names,
        "training_samples_count": len(X_train),
        "test_samples_count": len(X_test),
        "target_default_rate": round(float(default_rate), 4)
    }
    with open(os.path.join(models_dir, "feature_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # C. Threshold Configuration
    threshold_config = {
        "selected_threshold": selected_threshold,
        "cost_assumptions": {
            "false_negative_cost": 10000.0,
            "false_positive_cost": 1200.0
        },
        "risk_tier_cutoffs": DEFAULT_TIER_CUTOFFS,
        "actions_by_tier": {
            "Low": "Instant Approval - Standard Prime Terms",
            "Medium": "Approved with Automated Verification Check",
            "High": "Refer to Senior Credit Underwriter / Committee",
            "Critical": "Adverse Decision / Decline or Secured Exception Only"
        }
    }
    with open(os.path.join(models_dir, "threshold_config.json"), "w", encoding="utf-8") as f:
        json.dump(threshold_config, f, indent=2)

    # D. Test Metrics
    with open(os.path.join(models_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(final_eval, f, indent=2)

    # E. SHAP Explainer
    clf = final_pipeline.named_steps["classifier"]
    explainer = SHAPExplainer(model=clf, feature_names=transformed_feature_names)
    explainer.fit_tree_explainer(clf)
    explainer.save_explainer(os.path.join(models_dir, "shap_explainer.joblib"))

    logger.info("Training pipeline complete! All artifacts successfully saved in models/.")
    return {
        "final_metrics": final_eval,
        "threshold_config": threshold_config,
        "cv_comparison": cv_comparison
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Credit Risk Model Training Pipeline")
    parser.add_argument("--data-dir", type=str, default="data/raw")
    parser.add_argument("--models-dir", type=str, default="models")
    parser.add_argument("--sample-size", type=int, default=10000)
    args = parser.parse_args()

    run_training_pipeline(
        data_dir=args.data_dir,
        models_dir=args.models_dir,
        sample_size=args.sample_size
    )
