# AI Studio Interactive Preview & Mock Sandbox

This directory contains standalone mock data generators and test utilities for evaluating the Credit Risk UI without requiring heavy model training or downloading the 166 MB Home Credit dataset.

> **UI preview with sample data; not connected to the trained model.**

## Files:
- `mock_data.py`: Generates representative sample applicants across Low, Medium, High, and Critical risk tiers.
- `dashboard_preview.py`: Standalone CLI / script to inspect mock portfolio scoring and SHAP waterfall attributions.

For production execution using the real trained XGBoost pipeline, refer to `app/app.py`.
