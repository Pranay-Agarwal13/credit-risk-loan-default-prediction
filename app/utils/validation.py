"""
Input validation and schema enforcement for Credit Risk Streamlit App.
Validates batch CSV columns and single-applicant input ranges.
"""

from typing import Tuple, List, Dict, Any, Optional
import pandas as pd
import numpy as np

REQUIRED_BATCH_COLUMNS = [
    "SK_ID_CURR",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "EXT_SOURCE_2"
]

COLUMN_DEFINITIONS = {
    "SK_ID_CURR": {"label": "Applicant ID", "type": "Integer", "required": True},
    "AMT_INCOME_TOTAL": {"label": "Annual Income ($)", "type": "Float (> 0)", "required": True},
    "AMT_CREDIT": {"label": "Credit Amount ($)", "type": "Float (> 0)", "required": True},
    "AMT_ANNUITY": {"label": "Loan Annuity ($)", "type": "Float (> 0)", "required": True},
    "DAYS_BIRTH": {"label": "Age in Days (Negative)", "type": "Integer", "required": True},
    "DAYS_EMPLOYED": {"label": "Employment Tenure Days", "type": "Integer", "required": True},
    "EXT_SOURCE_2": {"label": "External Credit Score 2", "type": "Float (0.01-0.99)", "required": True},
    "NAME_CONTRACT_TYPE": {"label": "Contract Type", "type": "String", "required": False},
    "CODE_GENDER": {"label": "Gender", "type": "String (M/F)", "required": False},
    "FLAG_OWN_CAR": {"label": "Owns Car", "type": "String (Y/N)", "required": False},
    "FLAG_OWN_REALTY": {"label": "Owns Real Estate", "type": "String (Y/N)", "required": False},
    "NAME_EDUCATION_TYPE": {"label": "Education Level", "type": "String", "required": False},
    "EXT_SOURCE_1": {"label": "External Credit Score 1", "type": "Float", "required": False},
    "EXT_SOURCE_3": {"label": "External Credit Score 3", "type": "Float", "required": False},
    "BUREAU_ACTIVE_LOANS_COUNT": {"label": "Active Bureau Loans", "type": "Integer", "required": False},
    "BUREAU_AMT_CREDIT_SUM_DEBT_SUM": {"label": "Bureau Debt Balance ($)", "type": "Float", "required": False}
}

def validate_csv_schema_detailed(columns: List[str]) -> Dict[str, Any]:
    """
    Perform pre-scoring schema inspection on uploaded CSV headers.
    Returns structured feedback on required and optional columns.
    """
    cols_set = set(columns)
    missing_required = [col for col in REQUIRED_BATCH_COLUMNS if col not in cols_set]
    present_required = [col for col in REQUIRED_BATCH_COLUMNS if col in cols_set]
    missing_recommended = [col for col in RECOMMENDED_COLUMNS if col not in cols_set]
    present_recommended = [col for col in RECOMMENDED_COLUMNS if col in cols_set]

    checklist = []
    for col, meta in COLUMN_DEFINITIONS.items():
        is_present = col in cols_set
        checklist.append({
            "column": col,
            "label": meta["label"],
            "expected_type": meta["type"],
            "required": meta["required"],
            "status": "PRESENT" if is_present else ("MISSING_REQUIRED" if meta["required"] else "OPTIONAL_DEFAULTED")
        })

    is_valid = len(missing_required) == 0

    return {
        "is_valid": is_valid,
        "total_columns_detected": len(columns),
        "required_total": len(REQUIRED_BATCH_COLUMNS),
        "required_present_count": len(present_required),
        "required_missing_count": len(missing_required),
        "missing_required": missing_required,
        "present_required": present_required,
        "missing_recommended": missing_recommended,
        "present_recommended": present_recommended,
        "checklist": checklist
    }

def validate_batch_dataframe(df: pd.DataFrame) -> Tuple[bool, List[str], pd.DataFrame, pd.DataFrame]:
    """
    Validate uploaded batch CSV.
    Returns:
        (is_valid, error_messages, valid_df, invalid_df)
    """
    errors = []
    missing_required = [col for col in REQUIRED_BATCH_COLUMNS if col not in df.columns]
    
    if missing_required:
        errors.append(f"Missing mandatory columns: {', '.join(missing_required)}")
        return False, errors, pd.DataFrame(), df

    # Separate rows with valid numeric fields
    clean_df = df.copy()
    
    # Check for non-positive income and credit
    invalid_mask = (
        (clean_df["AMT_INCOME_TOTAL"] <= 0) |
        (clean_df["AMT_CREDIT"] <= 0) |
        (clean_df["AMT_ANNUITY"] <= 0) |
        (clean_df["SK_ID_CURR"].isna())
    )

    valid_df = clean_df[~invalid_mask].copy()
    invalid_df = clean_df[invalid_mask].copy()

    if len(valid_df) == 0:
        errors.append("No valid applicant rows found in uploaded file (all rows had non-positive values or missing IDs).")
        return False, errors, valid_df, invalid_df

    # Populate missing recommended columns with defaults
    for col in RECOMMENDED_COLUMNS:
        if col not in valid_df.columns:
            if "FLAG" in col:
                valid_df[col] = "N"
            elif col == "NAME_CONTRACT_TYPE":
                valid_df[col] = "Cash loans"
            elif col == "CODE_GENDER":
                valid_df[col] = "F"
            elif col == "NAME_EDUCATION_TYPE":
                valid_df[col] = "Secondary / secondary special"
            elif col == "NAME_FAMILY_STATUS":
                valid_df[col] = "Married"
            elif col == "NAME_HOUSING_TYPE":
                valid_df[col] = "House / apartment"
            elif "EXT_SOURCE" in col:
                valid_df[col] = 0.50
            else:
                valid_df[col] = 0

    return True, errors, valid_df, invalid_df

def validate_single_applicant(applicant_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate numeric ranges for single applicant form submission."""
    errors = []
    income = applicant_dict.get("AMT_INCOME_TOTAL", 0)
    credit = applicant_dict.get("AMT_CREDIT", 0)
    annuity = applicant_dict.get("AMT_ANNUITY", 0)

    if income < 10000:
        errors.append("Annual income must be at least $10,000.")
    if credit < 5000:
        errors.append("Credit amount must be at least $5,000.")
    if annuity <= 0:
        errors.append("Annuity payment must be greater than $0.")
    if annuity > income:
        errors.append("Annual annuity payment cannot exceed total declared annual income.")

    return len(errors) == 0, errors
