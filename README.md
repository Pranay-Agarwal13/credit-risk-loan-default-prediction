# Credit Risk & Loan Default Prediction System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DuckDB](https://img.shields.io/badge/SQL-DuckDB-yellow.svg)](https://duckdb.org/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange.svg)](https://xgboost.ai/)
[![SHAP](https://img.shields.io/badge/XAI-TreeSHAP-red.svg)](https://shap.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B.svg)](https://streamlit.io/)

> **Institutional Notice:** This system is an underwriter decision-support tool and does not make automated, unassisted loan approval decisions.

---

## 1. Business Problem & Executive Summary
In retail and consumer lending, evaluating default risk is essential to balance revenue growth with expected credit losses ($EL = PD \times EAD \times LGD$). 

When analyzing default datasets such as Kaggle's **Home Credit Default Risk**, default prevalence is only **~8.07%**. In this environment:
- Naive accuracy is misleading: a model predicting "No Default" for everyone achieves **91.93% accuracy**, but fails to catch a single bad loan, leading to severe charge-offs.
- False Negatives (funding a defaulting borrower) carry an average loss of **$10,000**, while False Positives (declining a good borrower) carry an opportunity cost of **$1,200** in interest margin.
- Standard models defaulting to a $0.50$ probability cutoff miss **71.6%** of defaults.

This repository provides an end-to-end, production-grade credit underwriting and machine learning framework that combines **DuckDB SQL cohort analytics**, a **leakage-safe preprocessing pipeline**, **cost-sensitive threshold optimization** (shifting the operational cutoff to $0.24$), **TreeSHAP explainability**, and a modern **multi-page Streamlit portal** (`st.navigation`).

---

## 2. Dataset Description & Download Instructions

The system is designed for the Kaggle **Home Credit Default Risk** dataset:
👉 [Download from Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk/data)

Place the downloaded CSV files inside `data/raw/`:
```bash
data/raw/
├── application_train.csv   # Primary dataset: 307,511 rows, 122 columns
└── bureau.csv              # Secondary dataset: 1,716,428 rows, 17 columns
```

*Note:* If running in a test environment without raw Kaggle CSVs, `src/data_loader.py` automatically generates high-fidelity synthetic samples with the identical schema, statistical moments, and 8.07% default rate, allowing the entire pipeline to run seamlessly out of the box.

---

## 3. Repository Architecture

```text
credit-risk-loan-default/
├── data/
│   ├── raw/                                 # Raw Kaggle CSVs (gitignored)
│   ├── sample_applicants.json               # Representative test profiles (Sarah, David, Marcus, Elena)
│   └── test_batch_sample.csv                # Sample CSV for batch upload testing
├── notebooks/
│   └── 01_eda_and_sql_analytics.ipynb       # EDA, target imbalance, correlations, DuckDB queries
├── sql/
│   ├── 01_default_rates_by_demographics.sql # Default rate by contract, education, gender, housing
│   ├── 02_financial_ratios_by_target.sql    # DTI, payment rate, external scores by target
│   ├── 03_top_risk_segments.sql             # Top 10 highest-risk applicant cohorts
│   └── 04_income_and_credit_bands.sql       # 2D portfolio matrix across income & loan sizes
├── src/
│   ├── __init__.py
│   ├── data_loader.py                       # DuckDB ingestion, SQL runner & synthetic generator
│   ├── feature_engineering.py               # DTI, annuity stress, bureau aggregates, leakage safety
│   ├── model_pipeline.py                    # ColumnTransformer, Imputer, Scaler, OHE, Model builders
│   ├── train.py                             # Stratified 5-Fold CV, hyperparameter fit, serialization
│   ├── evaluate.py                          # Metrics (ROC-AUC, PR-AUC), threshold optimization
│   ├── explainability.py                    # TreeSHAP explainer, waterfall generator, plain-English
│   └── utils.py                             # Cost-loss calculator, risk tiers, reproducibility seeds
├── models/
│   ├── model_pipeline.joblib                # Serialized preprocessing + XGBoost pipeline
│   ├── feature_metadata.json                # Feature lists, types, and engineered definitions
│   ├── threshold_config.json                # Selected 0.24 threshold & risk tier bands
│   ├── metrics.json                         # Test set ROC-AUC, PR-AUC, confusion matrix
│   └── segment_insights.csv                 # Pre-aggregated DuckDB query outputs
├── reports/
│   ├── model_comparison_metrics.csv         # Cross-validation & test comparison table
│   ├── model_card.md                        # Formal AI Model Card (ethics, bias, limitations)
│   └── resume_deliverables.md               # ATS resume bullets, LinkedIn pitch, 15 interview Q&As
├── app/
│   ├── app.py                               # Production Streamlit app with st.navigation
│   ├── pages/
│   │   ├── 1_Applicant_Risk_Assessment.py   # Single applicant intake form & SHAP waterfall
│   │   ├── 2_Batch_Scoring.py               # CSV batch upload, schema validation, download
│   │   ├── 3_Portfolio_Risk_Analytics.py    # Risk tier distribution & loan exposure charts
│   │   ├── 4_Model_Performance.py          # Interactive threshold slider, ROC/PR curves
│   │   ├── 5_SHAP_Explainability.py         # Global beeswarm, dependence curves, case studies
│   │   └── 6_Business_Insights.py           # DuckDB SQL segment analytical tables
│   ├── components/                          # UI cards, badges, SHAP plot wrappers
│   └── utils/                               # Artifact loader with @st.cache_resource, validation
├── preview/
│   ├── README.md                            # AI Studio preview documentation
│   ├── mock_data.py                         # Standalone mock generator for testing
│   └── dashboard_preview.py                 # Standalone script for quick UI verification
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 4. Installation & Quickstart

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/your-username/credit-risk-loan-default.git
cd credit-risk-loan-default

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run End-to-End Model Training Pipeline
Execute the complete training pipeline with 5-Fold Stratified Cross-Validation:
```bash
python src/train.py --sample-size 25000
```
This generates all artifacts in `models/`:
- `models/model_pipeline.joblib`
- `models/feature_metadata.json`
- `models/threshold_config.json`
- `models/metrics.json`
- `models/segment_insights.csv`

### Step 3: Launch the Production Streamlit Portal
```bash
streamlit run app/app.py
```
Open your browser at `http://localhost:8501`.

---

## 5. Model Evaluation & Benchmark Results

### 5-Fold Stratified Cross-Validation Comparison

| Model Architecture | Mean CV ROC-AUC | Mean CV PR-AUC | Test ROC-AUC | Test PR-AUC | Test F1-Score | Training Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Balanced)** | 0.6914 ± 0.0042 | 0.1850 ± 0.0051 | 0.6895 | 0.1821 | 0.2740 | ~14s |
| **Random Forest (Balanced)** | 0.7382 ± 0.0038 | 0.2291 ± 0.0047 | 0.7365 | 0.2274 | 0.3218 | ~68s |
| **Tuned XGBoost (`scale_pos_weight`)** | **0.7795 ± 0.0029** | **0.2831 ± 0.0039** | **0.7782** | **0.2814** | **0.3898** | ~33s |

### Decision Threshold Optimization ($0.50$ vs $0.24$)

| Decision Threshold | Defaulter Recall | Precision | Caught Defaults | Missed Defaults | Total Portfolio Loss |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0.50 (Standard Cutoff)** | 28.42% | 38.52% | 1,411 / 4,963 | 3,552 | $38.22M |
| **0.24 (Cost-Optimal Cutoff)** | **74.18%** | **26.45%** | **3,682 / 4,963** | **1,281** | **$25.04M** |
| **Net Financial Improvement** | **+45.76% Recall** | — | **+2,271 Caught** | **-2,271 Missed** | **+$13.18M Saved** |

---

## 6. Key SHAP Interpretability Findings
Using `shap.TreeExplainer`, we extracted global and local feature attributions:
1. **External Credit Bureau Scores (`EXT_SOURCE_1, 2, 3`):** Constitute over 45% of total model importance. Higher scores sharply reduce default log-odds.
2. **Credit-to-Income Leverage (`CREDIT_INCOME_RATIO`):** Exhibits non-linear risk expansion above $4.5\times$ debt-to-income.
3. **Employment Tenure (`DAYS_EMPLOYED`):** Borrowers with $< 1.5$ years on the job have higher default rates regardless of income level.
4. **Prior Credit Bureau Overdue:** Applicants with prior 30+ day delinquency have default rates nearly double baseline (13.88% vs 7.62%).

> **Disclaimer:** SHAP measures statistical associations learned from historical correlations and does not imply direct causal effects.

---

## 7. Policy Risk Tiers & Underwriting Actions

The system maps default probabilities into four calibrated underwriting tiers:

| Risk Tier | Probability Range | Action Recommendation | Portfolio Share |
| :--- | :---: | :--- | :---: |
| 🟢 **Low Risk** | $p < 0.10$ | Instant Approval with Prime Interest Rates | ~62% |
| 🟡 **Medium Risk** | $0.10 \le p < 0.24$ | Approved with Automated Verification Check | ~22% |
| 🟠 **High Risk** | $0.24 \le p < 0.50$ | Refer to Senior Credit Underwriter / Committee Review | ~11% |
| 🔴 **Critical Risk** | $p \ge 0.50$ | Adverse Decision / Automated Decline or Secured Exception | ~5% |

---

## 8. Limitations & Ethical Considerations
- **Fair Lending Compliance:** Designed to comply with ECOA and FCRA principles. Does not use race, religion, or prohibited demographic proxies.
- **Economic Regime Shifts:** Historical data reflects specific credit environments. Changes in interest rates or unemployment require model drift tracking via Population Stability Index (PSI).
- **Human-in-the-Loop:** All adverse underwriting actions require secondary human underwriter sign-off.
