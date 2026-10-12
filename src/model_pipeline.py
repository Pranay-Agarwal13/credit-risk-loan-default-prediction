"""
Model Pipeline Architecture for Credit Risk & Loan Default Prediction.
Encapsulates leakage-safe preprocessing inside ColumnTransformer and defines
Logistic Regression, Random Forest, and XGBoost estimators.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

from src.utils import logger, DEFAULT_SEED

# Core feature definitions
NUMERIC_FEATURES = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "CREDIT_INCOME_RATIO",
    "ANNUITY_INCOME_RATIO",
    "PAYMENT_RATE",
    "GOODS_CREDIT_RATIO",
    "INCOME_PER_FAMILY_MEMBER",
    "AGE_YEARS",
    "EMPLOYED_YEARS",
    "DAYS_EMPLOYED_PERC",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "EXT_SOURCES_MEAN",
    "EXT_SOURCES_STD",
    "BUREAU_DAYS_CREDIT_COUNT",
    "BUREAU_ACTIVE_LOANS_COUNT",
    "BUREAU_AMT_CREDIT_SUM_SUM",
    "BUREAU_AMT_CREDIT_SUM_DEBT_SUM",
    "BUREAU_DEBT_CREDIT_RATIO"
]

CATEGORICAL_FEATURES = [
    "NAME_CONTRACT_TYPE",
    "CODE_GENDER",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE"
]

def build_preprocessor(
    numeric_cols: Optional[List[str]] = None,
    categorical_cols: Optional[List[str]] = None
) -> ColumnTransformer:
    """
    Build scikit-learn ColumnTransformer ensuring leakage-free imputation and encoding.
    Fitted strictly on training folds.
    """
    num_cols = numeric_cols or NUMERIC_FEATURES
    cat_cols = categorical_cols or CATEGORICAL_FEATURES

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols)
        ],
        remainder="drop"
    )

    return preprocessor

def get_model_pipeline(
    model_type: str = "xgboost",
    scale_pos_weight: float = 11.38,  # (1 - 0.0807) / 0.0807 ~ 11.38 for Home Credit imbalance
    random_state: int = DEFAULT_SEED,
    preprocessor: Optional[ColumnTransformer] = None
) -> Pipeline:
    """
    Construct complete end-to-end Pipeline with preprocessing and classifier.
    
    Args:
        model_type: 'logistic_regression', 'random_forest', or 'xgboost'
        scale_pos_weight: Imbalance ratio for XGBoost positive class weighting
    """
    if preprocessor is None:
        preprocessor = build_preprocessor()

    if model_type == "logistic_regression":
        classifier = LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            C=0.1,
            random_state=random_state,
            solver="lbfgs"
        )
    elif model_type == "random_forest":
        classifier = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            min_samples_split=20,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1
        )
    elif model_type == "xgboost":
        if HAS_XGBOOST:
            classifier = xgb.XGBClassifier(
                n_estimators=250,
                max_depth=5,
                learning_rate=0.04,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=scale_pos_weight,
                random_state=random_state,
                eval_metric="auc",
                tree_method="hist",
                n_jobs=-1
            )
        else:
            logger.warning("XGBoost not installed. Using Random Forest as surrogate.")
            classifier = RandomForestClassifier(
                n_estimators=150,
                max_depth=12,
                class_weight="balanced",
                random_state=random_state
            )
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    return pipeline

def extract_feature_names(preprocessor: ColumnTransformer) -> List[str]:
    """Retrieve post-transformation feature names from fitted ColumnTransformer."""
    feature_names = []
    for name, transformer, cols in preprocessor.transformers_:
        if name == "num":
            feature_names.extend(cols)
        elif name == "cat":
            if hasattr(transformer, "named_steps") and "onehot" in transformer.named_steps:
                ohe = transformer.named_steps["onehot"]
                cats = ohe.get_feature_names_out(cols)
                feature_names.extend(cats)
            else:
                feature_names.extend(cols)
    return feature_names
