"""
Credit Risk & Loan Default Prediction System - Production Streamlit Dashboard.
Multipage entry point utilizing st.Page and st.navigation.
"""

import streamlit as st

# Global page layout and dark institutional styling
st.set_page_config(
    page_title="Credit Risk & Underwriting System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Multipage Navigation Setup using st.Page and st.navigation
pages = {
    "Underwriting Operations": [
        st.Page(
            "pages/1_Applicant_Risk_Assessment.py",
            title="Applicant Assessment",
            icon="👤",
            default=True
        ),
        st.Page(
            "pages/2_Batch_Scoring.py",
            title="Batch Scoring",
            icon="📁"
        ),
    ],
    "Risk Management & Analytics": [
        st.Page(
            "pages/3_Portfolio_Risk_Analytics.py",
            title="Portfolio Risk Analytics",
            icon="📊"
        ),
        st.Page(
            "pages/4_Model_Performance.py",
            title="Model Performance & Tuning",
            icon="🎯"
        ),
        st.Page(
            "pages/5_SHAP_Explainability.py",
            title="SHAP Explainability Studio",
            icon="🔍"
        ),
        st.Page(
            "pages/6_Business_Insights.py",
            title="Business Insights & SQL",
            icon="💡"
        ),
    ]
}

nav = st.navigation(pages)

# Sidebar brand header and institutional disclaimer
with st.sidebar:
    st.markdown("### 🏦 Credit Underwriting")
    st.caption("Default Risk & Policy Decision Support")
    st.markdown("---")
    st.caption("Active Model: **XGBoost Classifier**")
    st.caption("Operational Cutoff: **0.24**")
    st.caption("SQL Engine: **DuckDB In-Process**")
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 11px; color: #94A3B8; line-height: 1.4;">
            <strong>Advisory Notice:</strong><br>
            This tool supports credit-risk review and does not make automated loan approval decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

# Execute selected page
nav.run()
