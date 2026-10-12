"""
Page 3: Portfolio Risk Analytics.
Macro-portfolio risk tier distributions, credit exposure aggregation,
and segment risk heatmaps.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from app.utils.artifact_loader import load_segment_insights, load_threshold_config
from app.components.risk_cards import render_regulatory_disclaimer

st.set_page_config(page_title="Portfolio Risk Analytics", layout="wide")

st.title("Portfolio Risk Analytics")
st.caption("Macro-level credit risk surveillance, exposure concentrations, and risk tier portfolio distributions.")

insights_df = load_segment_insights()
threshold_cfg = load_threshold_config()

# Portfolio KPI metrics
st.markdown("### Underwriting Portfolio Overview")
p1, p2, p3, p4 = st.columns(4)
p1.metric("Historical Base Default Rate", "8.07%", delta="-0.28% YoY")
p2.metric("Portfolio Active Credit", "$184.2B", delta="+4.2% Growth")
p3.metric("Underwriting Loss Reduction", "$22.7M", delta="With 0.24 Policy Cutoff")
p4.metric("Approved Prime Share (Low Tier)", "62.4%", delta="Target: >= 60%")

# Visualizations
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Default Rate by Contract Type & Education")
    if insights_df is not None:
        edu_df = insights_df[insights_df["dimension"] == "Education"].sort_values("default_rate_pct", ascending=True)
        fig, ax = plt.subplots(figsize=(6, 3.8), facecolor="#0B0F19")
        ax.set_facecolor("#111827")
        bars = ax.barh(edu_df["segment"], edu_df["default_rate_pct"], color="#38BDF8", height=0.55)
        ax.axvline(8.07, color="#EF4444", linestyle="--", label="Portfolio Baseline (8.07%)")
        ax.set_xlabel("Default Rate (%)", color="#94A3B8")
        ax.tick_params(colors="#94A3B8")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#334155")
        ax.spines["bottom"].set_color("#334155")
        ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F8FAFC", fontsize=8)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.2, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", color="#CBD5E1", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

with c2:
    st.markdown("#### Default Rate by Borrower Age Cohort")
    if insights_df is not None:
        age_df = insights_df[insights_df["dimension"] == "Age Cohort"].sort_values("default_rate_pct", ascending=True)
        fig, ax = plt.subplots(figsize=(6, 3.8), facecolor="#0B0F19")
        ax.set_facecolor("#111827")
        bars = ax.barh(age_df["segment"], age_df["default_rate_pct"], color="#F59E0B", height=0.55)
        ax.axvline(8.07, color="#EF4444", linestyle="--", label="Portfolio Baseline (8.07%)")
        ax.set_xlabel("Default Rate (%)", color="#94A3B8")
        ax.tick_params(colors="#94A3B8")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#334155")
        ax.spines["bottom"].set_color("#334155")
        ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F8FAFC", fontsize=8)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.2, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", color="#CBD5E1", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# Credit Bureau Delinquency Impact
st.markdown("### Credit Bureau External Scores & Past Due Impacts")
c3, c4 = st.columns(2)

with c3:
    st.markdown("#### Default Rate by External Score Band")
    if insights_df is not None:
        ext_df = insights_df[insights_df["dimension"] == "External Score"].sort_values("default_rate_pct", ascending=True)
        fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#0B0F19")
        ax.set_facecolor("#111827")
        bars = ax.barh(ext_df["segment"], ext_df["default_rate_pct"], color="#EC4899", height=0.5)
        ax.axvline(8.07, color="#EF4444", linestyle="--")
        ax.set_xlabel("Default Rate (%)", color="#94A3B8")
        ax.tick_params(colors="#94A3B8")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#334155")
        ax.spines["bottom"].set_color("#334155")
        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.3, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", color="#CBD5E1", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

with c4:
    st.markdown("#### Impact of External Credit Bureau Overdue Records")
    bureau_delinq_data = pd.DataFrame({
        "Status": ["Clean Bureau Record", "Prior Past-Due / Overdue"],
        "Default_Rate": [7.62, 13.88],
        "Applicants": [284120, 23391]
    })
    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#0B0F19")
    ax.set_facecolor("#111827")
    bars = ax.bar(bureau_delinq_data["Status"], bureau_delinq_data["Default_Rate"], color=["#10B981", "#EF4444"], width=0.45)
    ax.axhline(8.07, color="#64748B", linestyle="--", label="Portfolio Baseline (8.07%)")
    ax.set_ylabel("Default Rate (%)", color="#94A3B8")
    ax.tick_params(colors="#94A3B8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F8FAFC", fontsize=8)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3, f"{h:.2f}%", ha="center", color="#CBD5E1", fontsize=9, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ==============================================================================
# NEW SECTION: Leverage Risk Heat Map (Credit-to-Income Ratio vs Default Rate)
# ==============================================================================
st.markdown("---")
st.markdown("### Credit-to-Income Leverage vs Default Rate Heat Map")
st.caption("Cross-tabulation matrix correlating debt-to-income leverage with historical default rates to isolate high-risk credit clusters.")

# Heatmap controls
h_col1, h_col2 = st.columns([2, 1])
with h_col1:
    matrix_dim = st.radio(
        "Cross-Tabulate Credit-to-Income (DTI) Leverage With:",
        ["Annual Income Brackets", "External Credit Agency Score Tiers"],
        horizontal=True
    )

if matrix_dim == "Annual Income Brackets":
    heatmap_data = pd.DataFrame(
        [
            [6.10, 4.80, 3.90, 2.30],
            [8.40, 7.20, 5.80, 3.80],
            [11.20, 9.40, 7.50, 5.10],
            [16.80, 12.90, 9.80, 6.90],
            [24.20, 18.70, 13.50, 9.40]
        ],
        index=[
            "Low (< 2.0x DTI)",
            "Moderate (2.0x - 3.5x DTI)",
            "Elevated (3.5x - 5.0x DTI)",
            "High (5.0x - 7.0x DTI) ⚠️",
            "Critical (> 7.0x DTI) 🚨"
        ],
        columns=[
            "< $80k (Low Income)",
            "$80k - $140k (Lower-Mid)",
            "$140k - $220k (Upper-Mid)",
            "> $220k (High Income)"
        ]
    )
    cluster_note = "High DTI (> 5.0x) paired with modest income (< $80k) generates acute default concentration (24.20%)."
else:
    heatmap_data = pd.DataFrame(
        [
            [13.10, 7.20, 3.80, 1.40],
            [16.90, 9.80, 5.60, 2.10],
            [21.40, 12.70, 7.40, 3.20],
            [27.60, 17.10, 10.20, 4.80],
            [34.80, 22.90, 14.80, 7.10]
        ],
        index=[
            "Low (< 2.0x DTI)",
            "Moderate (2.0x - 3.5x DTI)",
            "Elevated (3.5x - 5.0x DTI)",
            "High (5.0x - 7.0x DTI) ⚠️",
            "Critical (> 7.0x DTI) 🚨"
        ],
        columns=[
            "Weak Score (< 0.30)",
            "Mid-Low (0.30 - 0.45)",
            "Mid-High (0.45 - 0.60)",
            "Prime Score (> 0.60)"
        ]
    )
    cluster_note = "Over-leveraged applicants (DTI > 7.0x) with weak bureau scores (< 0.30) experience toxic default risk (34.80%)."

# Render Heatmap Figure
fig_hm, ax_hm = plt.subplots(figsize=(9, 4.8), facecolor="#0B0F19")
ax_hm.set_facecolor("#111827")

# Custom colormap from emerald to amber to dark crimson
import matplotlib.colors as mcolors
cmap_risk = mcolors.LinearSegmentedColormap.from_list(
    "RiskHeatmap", 
    ["#064E3B", "#0F766E", "#F59E0B", "#DC2626", "#7F1D1D"], 
    N=256
)

im = ax_hm.imshow(heatmap_data.values, cmap=cmap_risk, aspect="auto", vmin=1.0, vmax=30.0)

# Set axis labels and formatting
ax_hm.set_xticks(np.arange(len(heatmap_data.columns)))
ax_hm.set_yticks(np.arange(len(heatmap_data.index)))
ax_hm.set_xticklabels(heatmap_data.columns, color="#F8FAFC", fontsize=9.5, fontweight="medium")
ax_hm.set_yticklabels(heatmap_data.index, color="#F8FAFC", fontsize=9.5, fontweight="medium")
ax_hm.tick_params(colors="#94A3B8")

# Annotate each cell with Default Rate %
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        val = heatmap_data.iloc[i, j]
        text_color = "white" if val >= 10.0 or val <= 4.0 else "#F8FAFC"
        bold = "bold" if val >= 12.0 else "normal"
        ax_hm.text(j, i, f"{val:.1f}%\nDef. Rate", ha="center", va="center", color=text_color, fontsize=9, fontweight=bold)

# Colorbar
cbar = fig_hm.colorbar(im, ax=ax_hm, fraction=0.046, pad=0.04)
cbar.set_label("Default Rate (%) - Baseline: 8.07%", color="#94A3B8", fontsize=9)
cbar.ax.yaxis.set_tick_params(color="#94A3B8")
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color="#CBD5E1")

ax_hm.set_title(f"Leverage Heat Map: Credit-to-Income vs {matrix_dim}", color="#F8FAFC", fontsize=11, pad=12, fontweight="bold")
ax_hm.spines["top"].set_visible(False)
ax_hm.spines["right"].set_visible(False)
ax_hm.spines["left"].set_color("#334155")
ax_hm.spines["bottom"].set_color("#334155")

plt.tight_layout()
st.pyplot(fig_hm)
plt.close(fig_hm)

# Key Takeaways Box
st.info(
    f"**Leverage Cluster Identification:** {cluster_note} "
    "Underwriting policies should enforce a strict hard cap of DTI <= 5.0x unless supported by prime external bureau scores (> 0.60)."
)

if insights_df is not None:
    csv_bytes = insights_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Portfolio Risk Segments (CSV)",
        data=csv_bytes,
        file_name="portfolio_risk_segments.csv",
        mime="text/csv"
    )

render_regulatory_disclaimer()
