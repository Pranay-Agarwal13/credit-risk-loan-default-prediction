"""
Reusable UI metric cards and risk tier badges for Streamlit application.
"""

import streamlit as st

TIER_COLORS = {
    "Low": {"bg": "#064E3B", "text": "#34D399", "border": "#059669"},
    "Medium": {"bg": "#78350F", "text": "#FBBF24", "border": "#D97706"},
    "High": {"bg": "#7C2D12", "text": "#FB923C", "border": "#EA580C"},
    "Critical": {"bg": "#7F1D1D", "text": "#F87171", "border": "#DC2626"}
}

def render_risk_tier_badge(tier: str, probability: float):
    """Render a styled risk tier badge with probability."""
    colors = TIER_COLORS.get(tier, TIER_COLORS["Low"])
    st.markdown(
        f"""
        <div style="
            background-color: {colors['bg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #94A3B8;">
                    Assigned Credit Risk Tier
                </span>
                <h2 style="margin: 4px 0 0 0; color: {colors['text']}; font-weight: 700; font-size: 24px;">
                    {tier} Risk
                </h2>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #94A3B8;">
                    Default Probability
                </span>
                <h2 style="margin: 4px 0 0 0; color: #F8FAFC; font-family: monospace; font-size: 24px;">
                    {probability * 100:.2f}%
                </h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_underwriting_action_card(tier: str, action: str, decision: str):
    """Render underwriter recommendation callout."""
    colors = TIER_COLORS.get(tier, TIER_COLORS["Low"])
    st.markdown(
        f"""
        <div style="
            background-color: #111827;
            border-left: 4px solid {colors['border']};
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 20px;
        ">
            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">
                Policy Recommended Action: <span style="color: #F8FAFC;">{decision}</span>
            </div>
            <div style="color: #E2E8F0; font-size: 15px; font-weight: 500; margin-top: 4px;">
                {action}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_regulatory_disclaimer():
    """Render mandatory institutional compliance notice."""
    st.markdown(
        """
        <div style="
            background-color: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 6px;
            padding: 10px 14px;
            margin-top: 24px;
            font-size: 12px;
            color: #94A3B8;
            line-height: 1.5;
        ">
            <strong style="color: #CBD5E1;">Institutional Notice:</strong> 
            This tool supports credit-risk review and does not make automated loan approval decisions.
            All adverse actions require independent underwriter verification in compliance with Equal Credit Opportunity Act (ECOA) and FCRA guidelines.
        </div>
        """,
        unsafe_allow_html=True
    )
