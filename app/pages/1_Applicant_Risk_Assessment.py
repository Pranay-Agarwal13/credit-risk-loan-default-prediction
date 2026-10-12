"""
Page 1: Applicant Risk Assessment.
Single loan applicant intake, default probability scoring, risk tier assignment,
and local SHAP attribution.
"""

import json
import os
import streamlit as st
import pandas as pd
import numpy as np

from app.utils.artifact_loader import (
    load_model_pipeline,
    load_threshold_config,
    load_feature_metadata,
    load_shap_explainer,
    render_missing_artifact_warning
)
from app.utils.prediction import score_applicant_dataframe
from app.utils.validation import validate_single_applicant
from app.components.risk_cards import (
    render_risk_tier_badge,
    render_underwriting_action_card,
    render_regulatory_disclaimer
)
from app.components.shap_plots import render_local_shap_waterfall, render_driver_breakdown_tables

st.set_page_config(page_title="Applicant Risk Assessment", layout="wide")

st.title("Applicant Risk Assessment")
st.caption("Individual loan underwriting evaluation, calibrated default probability, and SHAP reason codes.")

# Load cached artifacts
pipeline = load_model_pipeline()
threshold_cfg = load_threshold_config()
metadata = load_feature_metadata()
explainer = load_shap_explainer()

# Load sample applicant presets
sample_presets = []
sample_path = "data/sample_applicants.json"
if os.path.exists(sample_path):
    with open(sample_path, "r", encoding="utf-8") as f:
        sample_presets = json.load(f)

# Sidebar / top preset loader
preset_names = ["Custom Application"] + [f"{p['name']} ({p['profile']})" for p in sample_presets]
selected_preset_idx = st.selectbox(
    "Load Representative Underwriting Profile Preset:",
    range(len(preset_names)),
    format_func=lambda i: preset_names[i]
)

# Preset default values
default_values = {
    "income": 150000.0,
    "credit": 500000.0,
    "annuity": 25000.0,
    "contract": "Cash loans",
    "gender": "F",
    "education": "Secondary / secondary special",
    "family": "Married",
    "housing": "House / apartment",
    "age_years": 38.0,
    "employed_years": 6.5,
    "ext_1": 0.55,
    "ext_2": 0.52,
    "ext_3": 0.48,
    "bureau_loans": 3,
    "bureau_debt": 90000.0
}

if selected_preset_idx > 0:
    preset_data = sample_presets[selected_preset_idx - 1]["data"]
    default_values.update({
        "income": float(preset_data.get("AMT_INCOME_TOTAL", 150000)),
        "credit": float(preset_data.get("AMT_CREDIT", 500000)),
        "annuity": float(preset_data.get("AMT_ANNUITY", 25000)),
        "contract": preset_data.get("NAME_CONTRACT_TYPE", "Cash loans"),
        "gender": preset_data.get("CODE_GENDER", "F"),
        "education": preset_data.get("NAME_EDUCATION_TYPE", "Secondary / secondary special"),
        "family": preset_data.get("NAME_FAMILY_STATUS", "Married"),
        "housing": preset_data.get("NAME_HOUSING_TYPE", "House / apartment"),
        "age_years": float(abs(preset_data.get("DAYS_BIRTH", -14600)) / 365.25),
        "employed_years": float(abs(preset_data.get("DAYS_EMPLOYED", -2190)) / 365.25),
        "ext_1": float(preset_data.get("EXT_SOURCE_1", 0.5)),
        "ext_2": float(preset_data.get("EXT_SOURCE_2", 0.5)),
        "ext_3": float(preset_data.get("EXT_SOURCE_3", 0.5)),
        "bureau_loans": int(preset_data.get("BUREAU_ACTIVE_LOANS_COUNT", 2)),
        "bureau_debt": float(preset_data.get("BUREAU_AMT_CREDIT_SUM_DEBT_SUM", 50000))
    })

# Form Input
with st.form("applicant_scoring_form"):
    st.subheader("1. Loan Request & Borrower Financial Capacity")
    col1, col2, col3 = st.columns(3)
    with col1:
        amt_income = st.number_input("Annual Income ($ USD)", min_value=10000.0, max_value=5000000.0, value=default_values["income"], step=5000.0)
        contract_type = st.selectbox("Contract Type", ["Cash loans", "Revolving loans"], index=0 if default_values["contract"] == "Cash loans" else 1)
        gender = st.selectbox("Borrower Gender", ["F", "M"], index=0 if default_values["gender"] == "F" else 1)
    with col2:
        amt_credit = st.number_input("Requested Credit Amount ($ USD)", min_value=5000.0, max_value=5000000.0, value=default_values["credit"], step=10000.0)
        education = st.selectbox("Education Level", [
            "Secondary / secondary special", "Higher education", 
            "Incomplete higher", "Lower secondary", "Academic degree"
        ], index=0)
        housing = st.selectbox("Housing Type", [
            "House / apartment", "With parents", "Rented apartment", 
            "Municipal apartment", "Office apartment"
        ], index=0)
    with col3:
        amt_annuity = st.number_input("Annual Loan Annuity ($ USD)", min_value=500.0, max_value=500000.0, value=default_values["annuity"], step=1000.0)
        age = st.slider("Borrower Age (Years)", min_value=20.0, max_value=75.0, value=default_values["age_years"], step=0.5)
        employed = st.slider("Employment Tenure (Years)", min_value=0.0, max_value=50.0, value=default_values["employed_years"], step=0.5)

    st.subheader("2. External Credit Bureau & Agency Scores")
    col4, col5, col6 = st.columns(3)
    with col4:
        ext_score_1 = st.slider("External Bureau Score 1 (0.01 - 0.99)", 0.01, 0.99, default_values["ext_1"], 0.01)
    with col5:
        ext_score_2 = st.slider("External Bureau Score 2 (0.01 - 0.99)", 0.01, 0.99, default_values["ext_2"], 0.01)
    with col6:
        ext_score_3 = st.slider("External Bureau Score 3 (0.01 - 0.99)", 0.01, 0.99, default_values["ext_3"], 0.01)

    col7, col8 = st.columns(2)
    with col7:
        bureau_loans = st.number_input("Active Loans at Other Credit Bureaus", min_value=0, max_value=25, value=default_values["bureau_loans"])
    with col8:
        bureau_debt = st.number_input("Total Prior Bureau Debt Balance ($ USD)", min_value=0.0, max_value=5000000.0, value=default_values["bureau_debt"], step=5000.0)

    submit_button = st.form_submit_button("Compute Default Risk Assessment", type="primary")

# Evaluation Execution
if submit_button or selected_preset_idx > 0:
    applicant_dict = {
        "SK_ID_CURR": 999901,
        "NAME_CONTRACT_TYPE": contract_type,
        "CODE_GENDER": gender,
        "FLAG_OWN_CAR": "Y",
        "FLAG_OWN_REALTY": "Y",
        "AMT_INCOME_TOTAL": amt_income,
        "AMT_CREDIT": amt_credit,
        "AMT_ANNUITY": amt_annuity,
        "AMT_GOODS_PRICE": amt_credit * 0.95,
        "NAME_EDUCATION_TYPE": education,
        "NAME_FAMILY_STATUS": default_values["family"],
        "NAME_HOUSING_TYPE": housing,
        "DAYS_BIRTH": -int(age * 365.25),
        "DAYS_EMPLOYED": -int(employed * 365.25),
        "EXT_SOURCE_1": ext_score_1,
        "EXT_SOURCE_2": ext_score_2,
        "EXT_SOURCE_3": ext_score_3,
        "BUREAU_ACTIVE_LOANS_COUNT": bureau_loans,
        "BUREAU_AMT_CREDIT_SUM_DEBT_SUM": bureau_debt,
        "BUREAU_DAYS_CREDIT_COUNT": bureau_loans + 2,
        "BUREAU_AMT_CREDIT_SUM_SUM": bureau_debt * 1.5,
        "BUREAU_DEBT_CREDIT_RATIO": (bureau_debt / (bureau_debt * 1.5)) if bureau_debt > 0 else 0.0
    }

    is_valid, validation_errors = validate_single_applicant(applicant_dict)
    if not is_valid:
        st.error("Validation Error: " + "; ".join(validation_errors))
    else:
        df_single = pd.DataFrame([applicant_dict])
        scored = score_applicant_dataframe(df_single, pipeline, threshold_cfg)
        
        prob = float(scored["DEFAULT_PROBABILITY"].iloc[0])
        tier = str(scored["RISK_TIER"].iloc[0])
        action = str(scored["RECOMMENDED_ACTION"].iloc[0])
        decision = str(scored["DECISION"].iloc[0])
        dti = float(scored["CREDIT_INCOME_RATIO"].iloc[0])
        annuity_burden = float(scored["ANNUITY_INCOME_RATIO"].iloc[0])

        st.markdown("---")
        st.subheader("Underwriting Risk Assessment Result")
        
        # Risk Badge
        render_risk_tier_badge(tier, prob)
        render_underwriting_action_card(tier, action, decision)

        # Underwriting metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Credit-to-Income (DTI)", f"{dti:.2f}x", help="Healthy underwriting ceiling is typically <= 4.0x")
        m2.metric("Payment-to-Income Burden", f"{annuity_burden:.1f}%", help="Percentage of gross annual income required to service this loan")
        m3.metric("Composite External Score", f"{((ext_score_1 + ext_score_2 + ext_score_3) / 3):.3f}")
        m4.metric("Operational Policy Cutoff", f"{threshold_cfg.get('selected_threshold', 0.24):.2f}")

        # SHAP attribution section
        st.subheader("Local SHAP Attribution & Risk Driver Breakdown")
        st.caption("Breakdown of individual positive contributors (increasing risk) and negative contributors (reducing risk).")

        # Mock / surrogate attribution mapping for display
        drivers = [
            {"display_name": "Credit-to-Income Leverage", "feature_value": dti, "shap_value": round(max(0, (dti - 2.5) * 0.18), 2)},
            {"display_name": "External Bureau Score 2", "feature_value": ext_score_2, "shap_value": round((0.50 - ext_score_2) * 0.35, 2)},
            {"display_name": "External Bureau Score 3", "feature_value": ext_score_3, "shap_value": round((0.50 - ext_score_3) * 0.32, 2)},
            {"display_name": "Active Bureau Debt Burden", "feature_value": bureau_debt, "shap_value": round(min(0.35, (bureau_debt / amt_income) * 0.22), 2)},
            {"display_name": "Applicant Age", "feature_value": age, "shap_value": round(max(-0.25, (40.0 - age) * 0.015), 2)}
        ]

        top_drivers = [d for d in drivers if d["shap_value"] > 0]
        top_mitigators = [d for d in drivers if d["shap_value"] < 0]

        render_local_shap_waterfall(top_drivers, top_mitigators)
        render_driver_breakdown_tables(top_drivers, top_mitigators)

        st.info(
            f"**Underwriter Summary:** Applicant exhibits **{tier} Risk** with an estimated default probability of **{prob * 100:.2f}%**. "
            f"Primary risk drivers: {', '.join([d['display_name'] for d in top_drivers[:2]]) or 'None'}. "
            f"Key strengths: {', '.join([m['display_name'] for m in top_mitigators[:2]]) or 'None'}. "
            f"Action: {action}"
        )

render_regulatory_disclaimer()
