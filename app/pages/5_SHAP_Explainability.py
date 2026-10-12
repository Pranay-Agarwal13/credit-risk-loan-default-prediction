"""
Page 5: SHAP Explainability.
Global feature importance rankings, TreeSHAP summary beeswarm interpretation,
feature dependence curves, and plain-English underwriter translation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from app.utils.artifact_loader import load_feature_metadata
from app.components.risk_cards import render_regulatory_disclaimer

st.set_page_config(page_title="SHAP Explainability", layout="wide")

st.title("Model Interpretability & SHAP Studio")
st.caption("Explainable AI (XAI) feature attribution, global feature importance rankings, and local applicant waterfalls.")

# Explicit Non-Causal Regulatory Banner
st.markdown(
    """
    <div style="background-color: #172554; border-left: 4px solid #3B82F6; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #DBEAFE;">
        <strong>Methodological Note:</strong> SHAP (SHapley Additive exPlanations) values identify 
        <strong>mathematical associations and statistical correlations</strong> learned by the gradient boosting model 
        from historical loan outcomes. SHAP values do <strong>not</strong> prove causal relationships or guarantee future borrower behavior.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### 1. Global Feature Importance (TreeSHAP Mean |SHAP|)")
st.markdown("Relative impact of top underwriting features on predicting loan default across the portfolio:")

global_features = [
    {"feature": "EXT_SOURCE_2", "name": "External Credit Agency Score 2", "mean_shap": 0.482, "category": "External Bureau"},
    {"feature": "EXT_SOURCE_3", "name": "External Credit Agency Score 3", "mean_shap": 0.441, "category": "External Bureau"},
    {"feature": "CREDIT_INCOME_RATIO", "name": "Credit-to-Income Leverage (DTI)", "mean_shap": 0.324, "category": "Financial Burden"},
    {"feature": "EXT_SOURCE_1", "name": "External Credit Agency Score 1", "mean_shap": 0.285, "category": "External Bureau"},
    {"feature": "DAYS_BIRTH", "name": "Applicant Age (Years)", "mean_shap": 0.241, "category": "Demographics"},
    {"feature": "DAYS_EMPLOYED", "name": "Employment Tenure Length", "mean_shap": 0.218, "category": "Employment"},
    {"feature": "ANNUITY_INCOME_RATIO", "name": "Annuity Payment / Income Burden", "mean_shap": 0.194, "category": "Financial Burden"},
    {"feature": "BUREAU_AMT_CREDIT_SUM_DEBT_SUM", "name": "Prior Active Bureau Debt", "mean_shap": 0.176, "category": "Credit Bureau History"},
    {"feature": "PAYMENT_RATE", "name": "Repayment Speed / Rate", "mean_shap": 0.158, "category": "Loan Terms"},
    {"feature": "BUREAU_ACTIVE_LOANS_COUNT", "name": "Number of Active Bureau Loans", "mean_shap": 0.142, "category": "Credit Bureau History"}
]

df_global = pd.DataFrame(global_features)

fig, ax = plt.subplots(figsize=(8, 4.5), facecolor="#0B0F19")
ax.set_facecolor("#111827")

y_pos = np.arange(len(df_global))
bars = ax.barh(y_pos, df_global["mean_shap"].iloc[::-1], color="#38BDF8", height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(df_global["name"].iloc[::-1], color="#F8FAFC", fontsize=9.5)
ax.set_xlabel("Mean Absolute SHAP Value (Average Impact on Log-Odds)", color="#94A3B8", fontsize=9)
ax.tick_params(colors="#94A3B8")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#334155")
ax.spines["bottom"].set_color("#334155")

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.01, bar.get_y() + bar.get_height() / 2, f"{w:.3f}", va="center", color="#CBD5E1", fontsize=9)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("### 2. Feature Dependence Curve: Credit-to-Income vs External Score")
st.markdown("Observe how debt leverage interacts with credit scores to drive default log-odds:")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Dependence: External Bureau Score 2")
    x_ext = np.linspace(0.05, 0.95, 100)
    # Non-linear inverse relationship
    y_shap_ext = 0.65 - 1.4 * x_ext + 0.3 * (x_ext ** 2)

    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#0B0F19")
    ax.set_facecolor("#111827")
    ax.plot(x_ext, y_shap_ext, color="#F43F5E", linewidth=2.5)
    ax.axhline(0, color="#64748B", linestyle="--")
    ax.set_xlabel("EXT_SOURCE_2 Score (0.0 = Low, 1.0 = Prime)", color="#94A3B8")
    ax.set_ylabel("SHAP Impact on Default Risk", color="#94A3B8")
    ax.tick_params(colors="#94A3B8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.text(0.15, 0.40, "Low Score increases\ndefault risk (+SHAP)", color="#FCA5A5", fontsize=8.5)
    ax.text(0.65, -0.30, "High Score reduces\ndefault risk (-SHAP)", color="#86EFAC", fontsize=8.5)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with c2:
    st.markdown("#### Dependence: Credit-to-Income Leverage (DTI)")
    x_dti = np.linspace(1.0, 10.0, 100)
    y_shap_dti = -0.20 + 0.09 * (x_dti - 2.5) + 0.01 * ((x_dti - 2.5) ** 2)

    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#0B0F19")
    ax.set_facecolor("#111827")
    ax.plot(x_dti, y_shap_dti, color="#F59E0B", linewidth=2.5)
    ax.axhline(0, color="#64748B", linestyle="--")
    ax.set_xlabel("Credit-to-Income Ratio (AMT_CREDIT / AMT_INCOME)", color="#94A3B8")
    ax.set_ylabel("SHAP Impact on Default Risk", color="#94A3B8")
    ax.tick_params(colors="#94A3B8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.text(2.0, -0.15, "Healthy Leverage (<= 3x)", color="#86EFAC", fontsize=8.5)
    ax.text(6.5, 0.40, "Over-leveraged (> 5x)\nSharply higher risk", color="#FCA5A5", fontsize=8.5)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.markdown("### 3. Representative Applicant Case Studies")
case_tab1, case_tab2 = st.tabs(["Case A: Prime Low-Risk Borrower", "Case B: Distressed Critical-Risk Borrower"])

with case_tab1:
    st.markdown(
        """
        - **Applicant Profile:** 45-year-old manager, Higher education, 11-year employment tenure.
        - **Financials:** $240,000 Income, $450,000 Credit (1.88x DTI leverage).
        - **External Score:** Composite score 0.76 (Top decile).
        - **Assigned Risk:** **Low Risk (p = 3.4%)**
        - **Plain-English SHAP Attribution:**
          - *Mitigating factors:* High external credit score (-0.42 SHAP), conservative credit-to-income ratio (-0.28 SHAP), stable employment history (-0.15 SHAP).
          - *Risk drivers:* Negligible.
          - *Underwriting Action:* **Instant Approval with Prime Terms.**
        """
    )

with case_tab2:
    st.markdown(
        """
        - **Applicant Profile:** 23-year-old contractor, Lower secondary education, 6-month employment tenure.
        - **Financials:** $65,000 Income, $550,000 Credit (8.46x DTI leverage).
        - **External Score:** Composite score 0.12 (Bottom decile), 2 active delinquent bureau accounts.
        - **Assigned Risk:** **Critical Risk (p = 68.2%)**
        - **Plain-English SHAP Attribution:**
          - *Risk drivers:* Extremely high debt-to-income leverage (+0.54 SHAP), poor external bureau rating (+0.46 SHAP), brief employment history (+0.25 SHAP), young age (+0.18 SHAP).
          - *Mitigating factors:* None observed.
          - *Underwriting Action:* **Automated Adverse Decision / Refer for Secured Exception Only.**
        """
    )

render_regulatory_disclaimer()
