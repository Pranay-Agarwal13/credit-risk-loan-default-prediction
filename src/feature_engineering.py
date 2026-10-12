"""
Feature Engineering module for Credit Risk & Loan Default Prediction.
Calculates domain-inspired underwriting ratios, external bureau aggregations,
and demographic metrics while ensuring strict leakage safety.
"""

from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd
from src.utils import logger

class FeatureEngineer:
    """Computes credit risk features and merges bureau aggregations."""

    def __init__(self):
        pass

    def compute_application_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute row-level domain features on application DataFrame.
        Works identically on training batches and single real-time inference applicants.
        """
        data = df.copy()

        # 1. Underwriting Leverage & Debt Service Ratios
        income = data["AMT_INCOME_TOTAL"].replace(0, np.nan)
        credit = data["AMT_CREDIT"].replace(0, np.nan)

        data["CREDIT_INCOME_RATIO"] = data["AMT_CREDIT"] / income
        data["ANNUITY_INCOME_RATIO"] = data["AMT_ANNUITY"] / income
        data["PAYMENT_RATE"] = data["AMT_ANNUITY"] / credit

        if "AMT_GOODS_PRICE" in data.columns:
            data["GOODS_CREDIT_RATIO"] = data["AMT_GOODS_PRICE"] / credit
        else:
            data["GOODS_CREDIT_RATIO"] = 1.0

        # 2. Demographic & Household Burden
        fam_members = data.get("CNT_FAM_MEMBERS", pd.Series(1, index=data.index)).replace(0, 1)
        data["INCOME_PER_FAMILY_MEMBER"] = data["AMT_INCOME_TOTAL"] / fam_members

        # 3. Age & Employment Tenure (converting negative days to positive years)
        if "DAYS_BIRTH" in data.columns:
            data["AGE_YEARS"] = np.abs(data["DAYS_BIRTH"]) / 365.25
        else:
            data["AGE_YEARS"] = 40.0

        if "DAYS_EMPLOYED" in data.columns:
            # Kaggle encoding: 365243 denotes unemployed/pensioner
            employed_days = data["DAYS_EMPLOYED"].copy()
            employed_days = np.where(employed_days > 0, 0, np.abs(employed_days))
            data["EMPLOYED_YEARS"] = employed_days / 365.25
            
            # Employment tenure as a percentage of adult life
            birth_days = np.abs(data.get("DAYS_BIRTH", 14600))
            data["DAYS_EMPLOYED_PERC"] = employed_days / np.maximum(birth_days, 1)
        else:
            data["EMPLOYED_YEARS"] = 5.0
            data["DAYS_EMPLOYED_PERC"] = 0.15

        # 4. External Credit Agency Aggregate Indicators
        ext_cols = [c for c in ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"] if c in data.columns]
        if ext_cols:
            ext_vals = data[ext_cols]
            data["EXT_SOURCES_MEAN"] = ext_vals.mean(axis=1)
            data["EXT_SOURCES_STD"] = ext_vals.std(axis=1).fillna(0)
            data["EXT_SOURCES_MIN"] = ext_vals.min(axis=1)
            data["EXT_SOURCES_MAX"] = ext_vals.max(axis=1)
        else:
            data["EXT_SOURCES_MEAN"] = 0.50
            data["EXT_SOURCES_STD"] = 0.0
            data["EXT_SOURCES_MIN"] = 0.50
            data["EXT_SOURCES_MAX"] = 0.50

        return data

    def aggregate_bureau(self, df_bureau: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate secondary credit bureau history per applicant (SK_ID_CURR).
        Computes active loans, aggregate debt, and delinquency history.
        """
        logger.info("Aggregating bureau credit history records...")
        
        # Group by applicant
        agg_funcs = {
            "DAYS_CREDIT": ["count", "max"],
            "AMT_CREDIT_SUM": ["sum", "mean"],
            "AMT_CREDIT_SUM_DEBT": ["sum"],
            "AMT_CREDIT_SUM_OVERDUE": ["sum", "max"],
            "CNT_CREDIT_PROLONG": ["sum"]
        }
        
        bureau_agg = df_bureau.groupby("SK_ID_CURR").agg(agg_funcs)
        # Flatten multi-level column index
        bureau_agg.columns = [f"BUREAU_{col}_{stat}".upper() for col, stat in bureau_agg.columns]
        bureau_agg = bureau_agg.reset_index()

        # Additional active credit loan counts
        if "CREDIT_ACTIVE" in df_bureau.columns:
            active_counts = (
                df_bureau[df_bureau["CREDIT_ACTIVE"] == "Active"]
                .groupby("SK_ID_CURR")
                .size()
                .rename("BUREAU_ACTIVE_LOANS_COUNT")
                .reset_index()
            )
            bureau_agg = pd.merge(bureau_agg, active_counts, on="SK_ID_CURR", how="left")
            bureau_agg["BUREAU_ACTIVE_LOANS_COUNT"] = bureau_agg["BUREAU_ACTIVE_LOANS_COUNT"].fillna(0)

        # Bureau debt to credit limit ratio
        total_credit = bureau_agg.get("BUREAU_AMT_CREDIT_SUM_SUM", 1).replace(0, np.nan)
        total_debt = bureau_agg.get("BUREAU_AMT_CREDIT_SUM_DEBT_SUM", 0)
        bureau_agg["BUREAU_DEBT_CREDIT_RATIO"] = total_debt / total_credit

        logger.info(f"Bureau aggregation complete: {len(bureau_agg):,} unique applicants.")
        return bureau_agg

    def merge_bureau_features(
        self, 
        df_app: pd.DataFrame, 
        df_bureau_agg: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """Merge aggregated bureau metrics onto application DataFrame."""
        if df_bureau_agg is None:
            # Populate default bureau columns if bureau table is not present
            df_merged = df_app.copy()
            df_merged["BUREAU_DAYS_CREDIT_COUNT"] = 3
            df_merged["BUREAU_ACTIVE_LOANS_COUNT"] = 1
            df_merged["BUREAU_AMT_CREDIT_SUM_SUM"] = df_merged["AMT_CREDIT"] * 0.8
            df_merged["BUREAU_AMT_CREDIT_SUM_DEBT_SUM"] = df_merged["AMT_CREDIT"] * 0.3
            df_merged["BUREAU_AMT_CREDIT_SUM_OVERDUE_SUM"] = 0.0
            df_merged["BUREAU_DEBT_CREDIT_RATIO"] = 0.375
            return df_merged

        df_merged = pd.merge(df_app, df_bureau_agg, on="SK_ID_CURR", how="left")
        
        # Fill zero for counts and debt for applicants with no prior bureau records
        count_cols = [c for c in df_merged.columns if "COUNT" in c]
        for col in count_cols:
            df_merged[col] = df_merged[col].fillna(0)

        debt_cols = [c for c in df_merged.columns if "SUM_SUM" in c or "DEBT" in c or "OVERDUE" in c]
        for col in debt_cols:
            df_merged[col] = df_merged[col].fillna(0)

        return df_merged
