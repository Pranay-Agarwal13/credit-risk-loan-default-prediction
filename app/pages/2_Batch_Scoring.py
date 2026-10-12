"""
Page 2: Batch Scoring.
Drag-and-drop CSV batch upload, schema validation, multi-tier risk classification,
and exportable scored portfolio records.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

from app.utils.artifact_loader import (
    load_model_pipeline,
    load_threshold_config,
    load_feature_metadata
)
from app.utils.prediction import score_applicant_dataframe
from app.utils.validation import validate_batch_dataframe, validate_csv_schema_detailed, REQUIRED_BATCH_COLUMNS
from app.components.risk_cards import render_regulatory_disclaimer

st.set_page_config(page_title="Batch Scoring", layout="wide")

st.title("Batch Application Scoring & Schema Inspector")
st.caption("Upload loan applicant batch CSVs with pre-flight schema validation, risk tier segmentation, and exportable decision records.")

pipeline = load_model_pipeline()
threshold_cfg = load_threshold_config()
metadata = load_feature_metadata()

# Quick sample buttons
col_up1, col_up2 = st.columns([2, 1])

with col_up1:
    uploaded_file = st.file_uploader(
        "Upload Loan Application Batch CSV:",
        type=["csv"],
        help="Upload CSV containing SK_ID_CURR, AMT_INCOME_TOTAL, AMT_CREDIT, AMT_ANNUITY, DAYS_BIRTH, DAYS_EMPLOYED, EXT_SOURCE_2"
    )

with col_up2:
    st.markdown("**Test Dataset Templates**")
    sample_csv_path = "data/test_batch_sample.csv"
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if os.path.exists(sample_csv_path):
            if st.button("Load Valid Batch", use_container_width=True):
                st.session_state["batch_df"] = pd.read_csv(sample_csv_path)
    with col_b2:
        if st.button("Test Invalid Schema", use_container_width=True, help="Simulate a CSV missing DAYS_BIRTH and EXT_SOURCE_2"):
            # Create a dataframe missing 2 required columns to demonstrate instant validator rejection
            if os.path.exists(sample_csv_path):
                sample_df = pd.read_csv(sample_csv_path)
                broken_df = sample_df.drop(columns=["DAYS_BIRTH", "EXT_SOURCE_2"], errors="ignore")
                st.session_state["batch_df"] = broken_df

if uploaded_file is not None:
    try:
        st.session_state["batch_df"] = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")

if "batch_df" in st.session_state:
    raw_df = st.session_state["batch_df"]
    
    # Run instant Pre-Flight Schema Inspection on uploaded columns
    schema_report = validate_csv_schema_detailed(list(raw_df.columns))

    st.markdown("### Pre-Flight CSV Schema Inspector")
    
    # Instant Feedback Banner
    if not schema_report["is_valid"]:
        st.error(
            f"❌ **Schema Validation Failed — Missing {schema_report['required_missing_count']} Mandatory Field(s)**\n\n"
            f"The model pipeline cannot score this file until all required columns are supplied.\n"
            f"- **Missing Required Columns:** `{', '.join(schema_report['missing_required'])}`\n"
            f"- **Detected Columns ({schema_report['total_columns_detected']}):** `{', '.join(raw_df.columns[:8])}...`"
        )
    else:
        st.success(
            f"✅ **Schema Verified — All {schema_report['required_total']} Required Columns Present** "
            f"({len(raw_df):,} applicant rows loaded, ready for underwriting evaluation)"
        )

    # Detailed Column Checklist Expander
    with st.expander("📋 View Detailed Column Schema Checklist", expanded=(not schema_report["is_valid"])):
        chk_cols = st.columns(2)
        half = len(schema_report["checklist"]) // 2
        with chk_cols[0]:
            st.markdown("**Mandatory Underwriting Inputs:**")
            for item in schema_report["checklist"][:half]:
                if item["required"]:
                    status_icon = "🟢 Present" if item["status"] == "PRESENT" else "🔴 MISSING"
                    st.markdown(f"- **`{item['column']}`** ({item['label']}): {status_icon}")
        with chk_cols[1]:
            st.markdown("**Secondary & Bureau Indicators:**")
            for item in schema_report["checklist"][half:]:
                status_icon = "🟢 Present" if item["status"] == "PRESENT" else ("🔴 MISSING" if item["required"] else "⚪ Optional (Auto-imputed)")
                st.markdown(f"- **`{item['column']}`** ({item['label']}): {status_icon}")

    # Prevent scoring execution if schema is invalid
    if not schema_report["is_valid"]:
        st.warning("⚠️ **Scoring Blocked:** Please supply the missing required columns or click 'Load Valid Batch' above to proceed.")
    else:
        # Validate row-level numeric integrity
        is_valid, validation_errors, valid_df, invalid_df = validate_batch_dataframe(raw_df)

        if len(invalid_df) > 0:
            st.warning(f"Flagged {len(invalid_df)} invalid rows (e.g. non-positive credit or missing IDs). These rows are quarantined.")

        with st.spinner("Scoring portfolio applications..."):
            scored_df = score_applicant_dataframe(valid_df, pipeline, threshold_cfg)

        # Portfolio Summary Metrics
        st.markdown("### Portfolio Scoring Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Scored Applicants", f"{len(scored_df):,}")
        m2.metric("Mean Portfolio Default Prob", f"{scored_df['DEFAULT_PROBABILITY'].mean() * 100:.2f}%")
        
        high_crit_count = int(scored_df["RISK_TIER"].isin(["High", "Critical"]).sum())
        m3.metric("High / Critical Risk Share", f"{high_crit_count} ({high_crit_count / len(scored_df) * 100:.1f}%)")
        
        flagged_count = int((scored_df["DECISION"] == "FLAGGED FOR REVIEW / DECLINE").sum())
        m4.metric("Flagged for Underwriter Review", f"{flagged_count} ({flagged_count / len(scored_df) * 100:.1f}%)")

        # Risk Tier Breakdown Counts
        tier_counts = scored_df["RISK_TIER"].value_counts().to_dict()
        st.markdown(
            f"""
            <div style="background-color: #111827; padding: 12px 16px; border-radius: 6px; margin: 12px 0 20px 0; display: flex; gap: 24px; font-size: 13px;">
                <span>🟢 <strong>Low Risk:</strong> {tier_counts.get('Low', 0)}</span>
                <span>🟡 <strong>Medium Risk:</strong> {tier_counts.get('Medium', 0)}</span>
                <span>🟠 <strong>High Risk:</strong> {tier_counts.get('High', 0)}</span>
                <span>🔴 <strong>Critical Risk:</strong> {tier_counts.get('Critical', 0)}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Filter controls - but by default SHOW ALL APPLICANTS
        st.markdown("### Scored Applicant Portfolio Records")
        f_col1, f_col2 = st.columns([1, 2])
        with f_col1:
            tier_filter = st.multiselect(
                "Filter by Risk Tier (All displayed by default):",
                ["Low", "Medium", "High", "Critical"],
                default=["Low", "Medium", "High", "Critical"]
            )
        with f_col2:
            search_query = st.text_input("Search by Applicant ID (SK_ID_CURR):", placeholder="e.g. 200001")

        display_df = scored_df[scored_df["RISK_TIER"].isin(tier_filter)].copy()
        if search_query:
            display_df = display_df[display_df["SK_ID_CURR"].astype(str).str.contains(search_query)]

        # Display full columns
        show_cols = [
            "SK_ID_CURR", "DEFAULT_PROBABILITY_PCT", "RISK_TIER", "DECISION", 
            "AMT_CREDIT", "AMT_INCOME_TOTAL", "CREDIT_INCOME_RATIO", "ANNUITY_INCOME_RATIO",
            "NAME_CONTRACT_TYPE", "RECOMMENDED_ACTION"
        ]
        available_cols = [c for c in show_cols if c in display_df.columns]

        st.dataframe(
            display_df[available_cols].style.format({
                "DEFAULT_PROBABILITY_PCT": "{:.2f}%",
                "AMT_CREDIT": "${:,.0f}",
                "AMT_INCOME_TOTAL": "${:,.0f}",
                "CREDIT_INCOME_RATIO": "{:.2f}x",
                "ANNUITY_INCOME_RATIO": "{:.1f}%"
            }),
            use_container_width=True,
            height=380
        )

        # Download button for complete scored results
        csv_download = scored_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Complete Scored Portfolio CSV",
            data=csv_download,
            file_name="scored_credit_portfolio_results.csv",
            mime="text/csv",
            type="primary"
        )
else:
    st.info("Upload a CSV file or click 'Load Pre-Populated Batch Sample' to begin batch scoring.")

render_regulatory_disclaimer()
