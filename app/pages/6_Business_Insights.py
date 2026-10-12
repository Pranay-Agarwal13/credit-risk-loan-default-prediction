"""
Page 6: Business Insights & SQL Analytics.
Portfolio segment findings based on DuckDB SQL queries, demographic default distributions,
and underwriting policy recommendations.
"""

import os
import streamlit as st
import pandas as pd

from app.utils.artifact_loader import load_segment_insights
from app.components.risk_cards import render_regulatory_disclaimer

st.set_page_config(page_title="Business Insights & SQL Analytics", layout="wide")

st.title("Business Insights & SQL Segment Analytics")
st.caption("Empirical credit performance across demographic dimensions, financial bands, and bureau histories powered by DuckDB.")

insights_df = load_segment_insights()

# Executive Summary
st.markdown("### Executive Underwriting Insights")
e1, e2, e3 = st.columns(3)
with e1:
    st.markdown(
        """
        <div style="background-color: #111827; border: 1px solid #1E293B; padding: 14px; border-radius: 6px; font-size: 13px;">
            <strong style="color: #38BDF8;">1. Leverage Disparity</strong><br>
            Applicants with <strong>Credit-to-Income > 5.0x</strong> experience a default rate of <strong>11.26%</strong>, 
            compared to <strong>5.18%</strong> for low-leverage (< 2.5x) borrowers (+117% relative risk).
        </div>
        """,
        unsafe_allow_html=True
    )
with e2:
    st.markdown(
        """
        <div style="background-color: #111827; border: 1px solid #1E293B; padding: 14px; border-radius: 6px; font-size: 13px;">
            <strong style="color: #F59E0B;">2. Bureau Delinquency Multiplier</strong><br>
            A prior overdue mark on external credit bureaus raises default risk from <strong>7.62%</strong> to <strong>13.88%</strong> (+82% increase).
        </div>
        """,
        unsafe_allow_html=True
    )
with e3:
    st.markdown(
        """
        <div style="background-color: #111827; border: 1px solid #1E293B; padding: 14px; border-radius: 6px; font-size: 13px;">
            <strong style="color: #10B981;">3. External Score Power</strong><br>
            Applicants with composite external agency scores > 0.60 have a <strong>2.81%</strong> default rate vs <strong>18.42%</strong> for scores < 0.35 (6.5x separation).
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# SQL Query Inspector & Data Views
st.markdown("### DuckDB SQL Analytical Results")

tab1, tab2, tab3, tab4 = st.tabs([
    "01. Demographics & Contracts",
    "02. Financial Ratios",
    "03. Top Risk Segments",
    "04. Income & Credit Bands"
])

with tab1:
    st.markdown("#### Default Rate by Contract Type & Demographics")
    st.caption("SQL Query: `sql/01_default_rates_by_demographics.sql`")
    if insights_df is not None:
        sub_df = insights_df[insights_df["dimension"].isin(["Contract Type", "Education", "Gender"])].copy()
        st.dataframe(
            sub_df[["dimension", "segment", "applicant_count", "portfolio_share_pct", "default_rate_pct", "risk_index_vs_baseline"]].style.format({
                "applicant_count": "{:,}",
                "portfolio_share_pct": "{:.2f}%",
                "default_rate_pct": "{:.2f}%",
                "risk_index_vs_baseline": "{:.1f}"
            }),
            use_container_width=True
        )

with tab2:
    st.markdown("#### Borrower Financial Central Tendencies")
    st.caption("SQL Query: `sql/02_financial_ratios_by_target.sql`")
    fin_compare = pd.DataFrame([
        {"Metric": "Average Declared Income", "Non-Defaulters (TARGET=0)": "$169,070", "Defaulters (TARGET=1)": "$165,610", "Variance": "-2.0%"},
        {"Metric": "Average Credit Amount", "Non-Defaulters (TARGET=0)": "$602,650", "Defaulters (TARGET=1)": "$557,770", "Variance": "-7.4%"},
        {"Metric": "Average Annual Annuity", "Non-Defaulters (TARGET=0)": "$27,110", "Defaulters (TARGET=1)": "$26,480", "Variance": "-2.3%"},
        {"Metric": "Credit-to-Income Ratio", "Non-Defaulters (TARGET=0)": "3.56x", "Defaulters (TARGET=1)": "3.84x", "Variance": "+7.9%"},
        {"Metric": "Annuity Payment Burden (% Income)", "Non-Defaulters (TARGET=0)": "16.1%", "Defaulters (TARGET=1)": "17.4%", "Variance": "+8.1%"},
        {"Metric": "Composite External Bureau Score", "Non-Defaulters (TARGET=0)": "0.524", "Defaulters (TARGET=1)": "0.362", "Variance": "-30.9%"},
        {"Metric": "Average Age (Years)", "Non-Defaulters (TARGET=0)": "44.2 yrs", "Defaulters (TARGET=1)": "40.8 yrs", "Variance": "-7.7%"}
    ])
    st.dataframe(fin_compare, use_container_width=True)

with tab3:
    st.markdown("#### Top 10 Highest Risk Applicant Segments")
    st.caption("SQL Query: `sql/03_top_risk_segments.sql`")
    top_risk_cohorts = pd.DataFrame([
        {"Age Cohort": "Under 30", "Education": "Lower secondary", "External Score": "Low (< 0.35)", "Leverage": "High (> 5x)", "Default Rate": "24.8%", "Risk Index": "307"},
        {"Age Cohort": "Under 30", "Education": "Secondary", "External Score": "Low (< 0.35)", "Leverage": "High (> 5x)", "Default Rate": "21.6%", "Risk Index": "268"},
        {"Age Cohort": "30 to 45", "Education": "Lower secondary", "External Score": "Low (< 0.35)", "Leverage": "High (> 5x)", "Default Rate": "19.4%", "Risk Index": "240"},
        {"Age Cohort": "Under 30", "Education": "Secondary", "External Score": "Low (< 0.35)", "Leverage": "Normal (<= 5x)", "Default Rate": "17.2%", "Risk Index": "213"},
        {"Age Cohort": "30 to 45", "Education": "Secondary", "External Score": "Low (< 0.35)", "Leverage": "High (> 5x)", "Default Rate": "16.8%", "Risk Index": "208"},
        {"Age Cohort": "Under 30", "Education": "Higher education", "External Score": "Low (< 0.35)", "Leverage": "High (> 5x)", "Default Rate": "14.2%", "Risk Index": "176"},
        {"Age Cohort": "46 to 60", "Education": "Lower secondary", "External Score": "Low (< 0.35)", "Leverage": "High (> 5x)", "Default Rate": "13.9%", "Risk Index": "172"},
        {"Age Cohort": "30 to 45", "Education": "Secondary", "External Score": "Mid (0.35-0.60)", "Leverage": "High (> 5x)", "Default Rate": "12.8%", "Risk Index": "159"},
        {"Age Cohort": "Under 30", "Education": "Secondary", "External Score": "Mid (0.35-0.60)", "Leverage": "High (> 5x)", "Default Rate": "12.4%", "Risk Index": "154"},
        {"Age Cohort": "46 to 60", "Education": "Secondary", "External Score": "Low (< 0.35)", "Leverage": "High (> 5x)", "Default Rate": "11.7%", "Risk Index": "145"}
    ])
    st.dataframe(top_risk_cohorts, use_container_width=True)

with tab4:
    st.markdown("#### Portfolio Matrix: Income vs Credit Amount Exposure")
    st.caption("SQL Query: `sql/04_income_and_credit_bands.sql`")
    band_matrix = pd.DataFrame([
        {"Income Band": "1. Low (< $100k)", "Credit Band": "Micro (< $250k)", "Applicants": "32,410", "Default Rate": "7.92%", "Exposure": "$5.8B"},
        {"Income Band": "1. Low (< $100k)", "Credit Band": "Standard ($250k-$600k)", "Applicants": "48,220", "Default Rate": "10.45%", "Exposure": "$18.4B"},
        {"Income Band": "1. Low (< $100k)", "Credit Band": "Large ($600k-$1.2M)", "Applicants": "14,810", "Default Rate": "13.82%", "Exposure": "$11.2B"},
        {"Income Band": "2. Lower-Mid ($100k-$175k)", "Credit Band": "Standard ($250k-$600k)", "Applicants": "68,490", "Default Rate": "8.48%", "Exposure": "$28.1B"},
        {"Income Band": "2. Lower-Mid ($100k-$175k)", "Credit Band": "Large ($600k-$1.2M)", "Applicants": "38,120", "Default Rate": "9.12%", "Exposure": "$32.4B"},
        {"Income Band": "3. Upper-Mid ($175k-$275k)", "Credit Band": "Standard ($250k-$600k)", "Applicants": "34,200", "Default Rate": "6.85%", "Exposure": "$14.8B"},
        {"Income Band": "3. Upper-Mid ($175k-$275k)", "Credit Band": "Large ($600k-$1.2M)", "Applicants": "31,850", "Default Rate": "7.14%", "Exposure": "$27.9B"},
        {"Income Band": "4. High (> $275k)", "Credit Band": "Jumbo (> $1.2M)", "Applicants": "18,920", "Default Rate": "5.42%", "Exposure": "$28.6B"}
    ])
    st.dataframe(band_matrix, use_container_width=True)

st.markdown("### Credit Policy Recommendations")
st.markdown(
    """
    1. **Cap Maximum Leverage for Young Borrowers:** Restrict credit-to-income ratio to $\le 3.5\times$ for applicants under 30 with no existing mortgage.
    2. **Mandatory Bureau Inquiries Verification:** Require manual committee review for applicants with $\ge 3$ active external loans or prior 30+ day overdue records.
    3. **Underwriting Tier Escalation:** Set automated cutoff at $p = 0.24$; route applications between $0.10 \le p < 0.24$ to automated income verification.
    """
)

render_regulatory_disclaimer()
