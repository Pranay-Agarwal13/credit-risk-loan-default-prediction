"""
SHAP visualization component for Streamlit application.
Renders local waterfall bar charts, positive vs negative contributor cards,
and plain-English underwriter explanation summaries.
"""

from typing import List, Dict, Any
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def render_local_shap_waterfall(top_drivers: List[Dict[str, Any]], top_mitigators: List[Dict[str, Any]]):
    """Render horizontal bar chart of local SHAP attributions."""
    items = []
    # Add negative (mitigating) and positive (increasing)
    for m in reversed(top_mitigators):
        items.append((m["display_name"], m["shap_value"], "#10B981"))
    for d in top_drivers:
        items.append((d["display_name"], d["shap_value"], "#EF4444"))

    if not items:
        st.info("No feature attributions available.")
        return

    labels = [it[0] for it in items]
    values = [it[1] for it in items]
    colors = [it[2] for it in items]

    fig, ax = plt.subplots(figsize=(8, max(3.5, len(labels) * 0.45)), facecolor="#0B0F19")
    ax.set_facecolor("#111827")

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, height=0.6, align="center")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, color="#F8FAFC", fontsize=10)
    ax.axvline(0, color="#475569", linewidth=1.0, linestyle="--")

    ax.tick_params(axis="x", colors="#94A3B8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.set_xlabel("SHAP Impact on Default Log-Odds (+ Increased Risk / - Mitigating)", color="#94A3B8", fontsize=9)

    for bar, val in zip(bars, values):
        x_pos = val + (0.01 if val >= 0 else -0.01)
        ha = "left" if val >= 0 else "right"
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2, f"{val:+.2f}", 
                va="center", ha=ha, color="#CBD5E1", fontsize=9, fontweight="bold")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def render_driver_breakdown_tables(top_drivers: List[Dict[str, Any]], top_mitigators: List[Dict[str, Any]]):
    """Render dual-column cards for risk drivers and mitigating factors."""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Primary Risk Drivers (Higher Risk)")
        if top_drivers:
            for item in top_drivers:
                st.markdown(
                    f"""
                    <div style="background-color: #1F2937; border-left: 3px solid #EF4444; padding: 8px 12px; margin-bottom: 8px; border-radius: 4px;">
                        <div style="font-weight: 600; font-size: 13px; color: #F8FAFC;">{item['display_name']}</div>
                        <div style="font-size: 12px; color: #94A3B8;">Observed Value: <span style="color: #E2E8F0; font-family: monospace;">{item['feature_value']:.2f}</span> | SHAP: <span style="color: #F87171; font-weight: bold;">+{item['shap_value']:.2f}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.caption("No significant adverse risk drivers detected.")

    with col2:
        st.markdown("#### Mitigating Factors (Lower Risk)")
        if top_mitigators:
            for item in top_mitigators:
                st.markdown(
                    f"""
                    <div style="background-color: #1F2937; border-left: 3px solid #10B981; padding: 8px 12px; margin-bottom: 8px; border-radius: 4px;">
                        <div style="font-weight: 600; font-size: 13px; color: #F8FAFC;">{item['display_name']}</div>
                        <div style="font-size: 12px; color: #94A3B8;">Observed Value: <span style="color: #E2E8F0; font-family: monospace;">{item['feature_value']:.2f}</span> | SHAP: <span style="color: #34D399; font-weight: bold;">{item['shap_value']:.2f}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.caption("No significant mitigating factors detected.")
