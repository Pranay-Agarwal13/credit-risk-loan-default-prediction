"""
Statistical plotting components for Model Performance and Portfolio Analytics.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def plot_confusion_matrix(cm: list, threshold: float):
    """Plot high-contrast confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(5, 4), facecolor="#0B0F19")
    ax.set_facecolor("#111827")

    cm_arr = np.array(cm)
    im = ax.imshow(cm_arr, interpolation="nearest", cmap="Blues")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted Repaid", "Predicted Default"], color="#E2E8F0")
    ax.set_yticklabels(["Actual Repaid", "Actual Default"], color="#E2E8F0")

    thresh = cm_arr.max() / 2.0
    for i in range(2):
        for j in range(2):
            val = cm_arr[i, j]
            color = "white" if val > thresh else "#94A3B8"
            ax.text(j, i, f"{val:,}", ha="center", va="center", color=color, fontsize=12, fontweight="bold")

    ax.set_title(f"Confusion Matrix @ Threshold = {threshold:.2f}", color="#F8FAFC", fontsize=11, pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def plot_threshold_curves(thresholds: np.ndarray, precisions: np.ndarray, recalls: np.ndarray, f1s: np.ndarray, selected_t: float):
    """Plot Precision, Recall, and F1 across decision thresholds."""
    fig, ax = plt.subplots(figsize=(7, 3.8), facecolor="#0B0F19")
    ax.set_facecolor("#111827")

    ax.plot(thresholds, recalls, label="Recall (Defaulter Capture Rate)", color="#38BDF8", linewidth=2)
    ax.plot(thresholds, precisions, label="Precision (True Defaulters / Flagged)", color="#F59E0B", linewidth=2)
    ax.plot(thresholds, f1s, label="F1-Score", color="#10B981", linewidth=2, linestyle="--")

    ax.axvline(selected_t, color="#EF4444", linestyle=":", linewidth=2, label=f"Selected Threshold ({selected_t:.2f})")
    ax.axvline(0.50, color="#64748B", linestyle="--", linewidth=1.5, label="Standard Default (0.50)")

    ax.set_xlabel("Decision Probability Threshold", color="#94A3B8")
    ax.set_ylabel("Metric Score", color="#94A3B8")
    ax.set_ylim(0, 1.05)
    ax.tick_params(colors="#94A3B8")
    ax.grid(True, color="#1F2937", linestyle="--", alpha=0.7)
    ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F8FAFC", fontsize=9)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
