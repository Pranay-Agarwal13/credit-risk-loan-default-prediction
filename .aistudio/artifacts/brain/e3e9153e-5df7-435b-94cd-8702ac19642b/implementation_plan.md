# Credit Risk & Loan Default Prediction System

A production-quality credit underwriting and default risk forecasting system built on the Kaggle Home Credit Default Risk dataset. The system integrates DuckDB SQL segment analytics, a leakage-safe scikit-learn preprocessing pipeline, class-imbalance-resilient XGBoost modeling, cost-sensitive threshold optimization, TreeSHAP feature-attribution interpretability, a complete production Streamlit dashboard (`app/app.py`), and a lightweight Google AI Studio interactive preview workbench.

### User Review & Critical Decisions

> [!IMPORTANT]
> The following architectural decisions and user refinements are confirmed:
> - **Multipage Streamlit Architecture**: Built with Streamlit's modern `st.Page` and `st.navigation` router with dedicated page modules in `app/pages/`, modular UI cards in `app/components/`, and utilities in `app/utils/`.
> - **Resource Caching Contract (`@st.cache_resource`)**: All heavy model artifacts (`model_pipeline.joblib`, `feature_metadata.json`, `threshold_config.json`, `shap_explainer.joblib`, `metrics.json`, `segment_insights.csv`) are cached in memory across reruns.
> - **Graceful Artifact Fallbacks**: If any model artifact in `models/` is missing, the dashboard presents actionable terminal setup instructions (`python src/train.py`) rather than crashing.
> - **Practical TreeSHAP Strategy**: Global SHAP values are precomputed on a representative validation sample; local SHAP waterfall attributions are generated on demand per applicant, split into positive vs negative risk drivers with plain-English associations (noting non-causality).
> - **Batch Validation & Full Inclusion**: All applicants across Low, Medium, High, and Critical risk tiers are retained and exportable. Missing and invalid schema fields are validated gracefully.
> - **Dual Delivery Separation**:
>   - `app/app.py`: Production Streamlit app using the trained model and artifacts.
>   - `preview/` + AI Studio React UI: Fast interactive preview using sample data clearly labeled: *"UI preview with sample data; not connected to the trained model."*
> - **Regulatory Disclaimer**: Prominently displayed:
>   *"This tool supports credit-risk review and does not make automated loan approval decisions."*

---

## 1. Overview & Core Concept

- **What It Does**: Evaluates consumer loan applications to predict the probability of default or payment difficulty (`TARGET = 1` vs `TARGET = 0`), categorizes applications into four calibrated risk tiers (Low, Medium, High, Critical), recommends tier-specific underwriting actions (Standard Approval, Verification Check, Manual Credit Committee Review, Decline), and delivers plain-English risk driver summaries backed by SHAP values.
- **Target Audience / Persona**: Credit risk officers, senior underwriters, and portfolio risk managers who require transparent, defensible, and audit-ready credit risk signals.
- **Key Value**: Balances loan default prevention (reducing expected credit losses) against good-customer false rejections (preserving interest margin and customer relationships) via cost-based decision thresholding and model transparency.

---

## 2. User Experience & Visual Design

### Multipage Streamlit Application Pages (`app/pages/`)
1. **`1_Applicant_Risk_Assessment.py`**:
   - Single applicant intake form with loan parameters, financial burden ratios, and credit bureau records.
   - Calculates default probability, assigns calibrated risk tier, and presents the top positive and negative risk drivers in plain English.
2. **`2_Batch_Scoring.py`**:
   - Drag-and-drop CSV batch upload with column schema validation.
   - Flags invalid rows while scoring all valid rows across all risk tiers (Low, Medium, High, Critical).
   - Generates portfolio risk summary statistics and provides a 1-click download of the complete scored CSV.
3. **`3_Portfolio_Risk_Analytics.py`**:
   - High-density visual portfolio distribution: default rates across loan contract types, employment tenure, and bureau exposure.
   - Risk tier breakdown and loan volume exposure heatmaps.
4. **`4_Model_Performance.py`**:
   - Interactive threshold simulator showing the trade-off between Precision, Recall, F1-score, and false-negative vs false-positive business costs.
   - Displays ROC-AUC curves, Precision-Recall curves, and confusion matrices comparing Logistic Regression, Random Forest, and XGBoost.
5. **`5_SHAP_Explainability.py`**:
   - Global feature importance beeswarm plots, dependence plots (e.g. `EXT_SOURCE_2`, `CREDIT_TO_INCOME_RATIO`), and local applicant waterfall breakdowns.
   - Explicit disclaimer that SHAP identifies model associations, not causal effects.
6. **`6_Business_Insights.py`**:
   - Interactive SQL segment viewer displaying DuckDB analytical query results (default rate by contract, gender, income bracket, education, and bureau overdue records).

### Visual Identity & Theme
- **Aesthetic Direction**: High-density financial risk terminal with dark professional theme, strict typography, and zero visual clutter.
- **Color Palette**:
  - Background Canvas: Slate Dark `#0B0F19` with container panels `#111827` and hairline borders `#1F2937`.
  - Risk Tier Accents:
    - Low Risk: Emerald `#059669`
    - Medium Risk: Amber `#D97706`
    - High Risk: Orange `#EA580C`
    - Critical Risk: Crimson `#DC2626`
- **Typography & Formatting**: Clean sans-serif headers paired with strict tabular figures (`tabular-nums font-mono`) for all financial metrics, debt ratios, and risk scores.

---

## 3. Artifact Contract & Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Home Credit Default Risk Data Pipeline               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
   application_train.csv                                bureau.csv
  (307,511 rows, 122 cols)                       (1,716,428 rows, 17 cols)
           │                                                 │
           │                                      DuckDB / Pandas Aggregation
           │                                      • Total active credits
           │                                      • Total debt & credit limit
           │                                      • Max days past due (DPD)
           └────────────────────────┬────────────────────────┘
                                    │
                                    ▼
                     Feature Engineering & Preprocessing
         • Debt-to-Income, Annuity-to-Income, Payment Burden
         • External Scores aggregates (mean, min, std of EXT_SOURCE_1/2/3)
         • Age & Employment tenure years, Income per family member
                                    │
               ┌────────────────────┴────────────────────┐
               ▼                                         ▼
   Leakage-Safe Preprocessing Pipeline          DuckDB Analytics Warehouse
  (ColumnTransformer, Imputer, Scaler, OHE)    (Default rates by contract,
               │                                income bands, risk segments)
               ▼
     Model Training & Cross-Validation
   • Logistic Regression (Interpretable baseline)
   • Random Forest (Bagging ensemble)
   • XGBoost (Gradient boosting with scale_pos_weight)
               │
               ▼
    Cost-Sensitive Threshold Tuning & Risk Tiers
    (Low < 0.10, Medium 0.10-0.25, High 0.25-0.50, Critical > 0.50)
               │
               ▼
       SHAP Explainability Engine (TreeExplainer, Waterfall plots)
               │
               ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │                    Artifacts in models/                         │
   │  • model_pipeline.joblib   • feature_metadata.json              │
   │  • threshold_config.json   • shap_explainer.joblib / sample     │
   │  • metrics.json            • segment_insights.csv               │
   └───────────────────┬─────────────────────────────────────────────┘
                       │
       ┌───────────────┴────────────────────────────────┐
       ▼                                                ▼
Production Streamlit App (`app/`)           Interactive AI Studio Preview
• Loaded via `@st.cache_resource`           • Fast in-browser React workbench
• Real pipeline & SHAP inference            • Mock data labeled as UI preview
• Full batch CSV scoring & exports          • Threshold & SQL exploration
```

### Exact Artifact Contract in `models/`
- **`model_pipeline.joblib`**: Complete scikit-learn pipeline bundling the `ColumnTransformer` (median imputers, standard/robust scalers, one-hot encoders) and the trained `XGBClassifier`.
- **`feature_metadata.json`**: Feature list, numeric ranges, categorical levels, and engineered ratio formulas.
- **`threshold_config.json`**: Selected decision threshold (e.g. 0.24) and risk-tier boundaries:
  - Low Risk: $p < 0.10$ (Action: Instant Approve / Standard Terms)
  - Medium Risk: $0.10 \le p < 0.25$ (Action: Standard Verification)
  - High Risk: $0.25 \le p < 0.50$ (Action: Manual Review / Enhanced Diligence)
  - Critical Risk: $p \ge 0.50$ (Action: Decline / Exception Only)
- **`shap_explainer.joblib`** & **`shap_values_sample.parquet`**: Precomputed TreeExplainer and validation sample SHAP matrix for fast global plotting and on-demand local waterfalls.
- **`metrics.json`**: Test-set ROC-AUC, PR-AUC, precision, recall, F1, and confusion matrix values.
- **`segment_insights.csv`**: Pre-aggregated DuckDB segment query outputs for instant dashboard analytics.

---

## 4. Complete Repository Structure

```
credit-risk-loan-default/
├── data/
│   ├── raw/                                 # Downloaded raw CSV files (gitignored)
│   │   ├── application_train.csv
│   │   └── bureau.csv
│   ├── processed/                           # Aggregated parquet / duckdb database
│   ├── sample_applicants.json               # Representative sample applicants
│   └── test_batch_sample.csv                # Sample batch CSV for upload testing
├── notebooks/
│   └── 01_eda_and_sql_analytics.ipynb       # Complete EDA, target imbalance, correlations, SQL
├── sql/
│   ├── 01_default_rates_by_demographics.sql # Default rate by contract, gender, education, etc.
│   ├── 02_financial_ratios_by_target.sql    # Income, credit, annuity, and ratio comparisons
│   ├── 03_top_risk_segments.sql             # Top 10 highest-risk applicant cohorts
│   └── 04_income_and_credit_bands.sql       # Distribution across income and credit bands
├── src/
│   ├── __init__.py
│   ├── data_loader.py                       # DuckDB ingestion, raw CSV reading & schema checks
│   ├── feature_engineering.py               # Financial ratios, bureau aggregations, pipelines
│   ├── model_pipeline.py                    # ColumnTransformer, Imputer, Scaler, OHE, Models
│   ├── train.py                             # Stratified K-Fold CV, hyperparameter tuning, model fit
│   ├── evaluate.py                          # Metrics (ROC-AUC, PR-AUC), threshold optimization
│   ├── explainability.py                    # SHAP TreeExplainer, waterfall generator, summaries
│   └── utils.py                             # Cost matrix calculation, random seeds, logging
├── models/
│   ├── model_pipeline.joblib
│   ├── feature_metadata.json
│   ├── threshold_config.json
│   ├── shap_explainer.joblib
│   ├── metrics.json
│   └── segment_insights.csv
├── reports/
│   ├── model_comparison_metrics.csv         # Cross-validation and held-out test metrics
│   ├── model_card.md                        # Model Card (intended use, bias, data, metrics)
│   ├── resume_deliverables.md               # Resume bullets, LinkedIn post, 15 interview Q&As
│   └── figures/                             # Saved plots (ROC curve, PR curve, SHAP summary)
├── app/
│   ├── app.py                               # Main Streamlit app with st.navigation & st.Page
│   ├── pages/
│   │   ├── 1_Applicant_Risk_Assessment.py   # Single applicant risk scoring & SHAP
│   │   ├── 2_Batch_Scoring.py               # Batch CSV upload, validation, download
│   │   ├── 3_Portfolio_Risk_Analytics.py    # Risk tier distribution & loan exposure
│   │   ├── 4_Model_Performance.py          # Threshold simulator, ROC/PR curves
│   │   ├── 5_SHAP_Explainability.py         # Global & local SHAP visualizations
│   │   └── 6_Business_Insights.py           # DuckDB SQL segment analytics
│   ├── components/
│   │   ├── risk_cards.py                    # Metric scorecards and risk tier badges
│   │   ├── shap_plots.py                    # Waterfall and beeswarm plot wrappers
│   │   └── charts.py                        # Confusion matrices and distribution plots
│   └── utils/
│       ├── artifact_loader.py               # @st.cache_resource loader with graceful fallbacks
│       ├── prediction.py                    # Pipeline scoring & risk tier categorization
│       └── validation.py                    # CSV schema & applicant range validators
├── preview/
│   ├── README.md                            # Instructions for AI Studio UI preview
│   ├── mock_data.py                         # Standalone mock generator for testing
│   └── dashboard_preview.py                 # Standalone preview script
├── src_preview/                             # AI Studio React preview application
│   └── (App.tsx and components)             # Full interactive in-browser preview dashboard
├── .gitignore
├── requirements.txt
└── README.md                                # Production-grade project documentation
```

### Exact Dataset Files to Download

From the Kaggle competition page ([Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk/data)):

1. **`application_train.csv`** *(Primary Dataset, Mandatory)*:
   - Place in `data/raw/application_train.csv`
   - Size: ~166 MB (307,511 rows, 122 columns).
   - Target column: `TARGET` (0 = loan repaid, 1 = payment difficulties / default).
   - Key features: Demographics, income, annuity, credit amount, employment days, and external credit bureau scores (`EXT_SOURCE_1`, `EXT_SOURCE_2`, `EXT_SOURCE_3`).
2. **`bureau.csv`** *(Secondary Dataset, Confirmed)*:
   - Place in `data/raw/bureau.csv`
   - Size: ~374 MB (1,716,428 rows, 17 columns).
   - Foreign Key: `SK_ID_CURR` linking back to applicants.
   - Features: Previous loans recorded at other credit bureaus, `CREDIT_ACTIVE`, `DAYS_CREDIT`, `AMT_CREDIT_SUM`, `AMT_CREDIT_SUM_DEBT`, `AMT_CREDIT_SUM_OVERDUE`.

---

## 5. Step-by-Step Build Order

1. **Phase 1: Environment & Repository Infrastructure**
   - Configure `.gitignore` (ignoring raw CSVs, large checkpoints, and virtualenvs).
   - Write comprehensive `requirements.txt` with pinned dependencies (`duckdb`, `pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `streamlit`, `matplotlib`, `seaborn`, `joblib`).
2. **Phase 2: DuckDB Data Layer & Production SQL Query Suite**
   - Implement `src/data_loader.py` supporting DuckDB and pandas.
   - Author standard analytical SQL queries in `sql/` (01 demographics, 02 financial ratios, 03 high-risk segments, 04 credit bands).
   - Author Jupyter Notebook `notebooks/01_eda_and_sql_analytics.ipynb` detailing target imbalance (8.07%), missingness patterns, and domain distributions.
   - Generate `models/segment_insights.csv` from SQL queries for pre-loaded instant analytics.
3. **Phase 3: Domain Feature Engineering & Leakage-Safe Pipelines**
   - Implement `src/feature_engineering.py` computing financial ratios (`CREDIT_INCOME_RATIO`, `ANNUITY_INCOME_RATIO`, `PAYMENT_RATE`, `EXT_SOURCES_MEAN`, `DAYS_EMPLOYED_PERC`) and `bureau.csv` aggregations.
   - Implement `src/model_pipeline.py` with `ColumnTransformer` (median imputers, robust scalers, one-hot encoders).
4. **Phase 4: Model Training, Cross-Validation & Threshold Tuning**
   - Implement `src/train.py` training Logistic Regression, Random Forest, and XGBoost using Stratified K-Fold CV.
   - Implement `src/evaluate.py` calculating ROC-AUC, PR-AUC, Precision, Recall, F1, and cost-curve threshold optimization.
   - Generate production artifacts: `models/model_pipeline.joblib`, `models/feature_metadata.json`, `models/threshold_config.json`, and `models/metrics.json`.
5. **Phase 5: SHAP Interpretability & Natural-Language Translation**
   - Implement `src/explainability.py` using `shap.TreeExplainer` on the XGBoost model.
   - Precompute validation sample SHAP values and save `models/shap_explainer.joblib` / `models/shap_values_sample.parquet`.
   - Implement on-demand local applicant waterfall generator with plain-English positive/negative push factors.
6. **Phase 6: Multipage Production Streamlit Dashboard (`app/`)**
   - Implement `app/utils/artifact_loader.py` with `@st.cache_resource` and graceful missing-artifact recovery notices.
   - Implement `app/utils/validation.py` for batch CSV validation and applicant range checking.
   - Implement `app/components/` (`risk_cards.py`, `shap_plots.py`, `charts.py`).
   - Implement `app/pages/` (all 6 individual page modules) and `app/app.py` navigation with `st.navigation`.
   - Provide `test_batch_sample.csv` and `sample_applicants.json` for immediate testing.
7. **Phase 7: Google AI Studio Interactive Preview Dashboard**
   - Build a sleek, responsive React/TypeScript workbench in `src/` replicating all 6 pages with sample portfolio data across all risk tiers, interactive threshold sliders, waterfall charts, and SQL segment insights.
   - Mark prominently: *"UI preview with sample data; not connected to the trained model."*
8. **Phase 8: Documentation, Model Card & Career Deliverables**
   - Write comprehensive `README.md` with complete setup instructions, dataset links, and execution commands (`streamlit run app/app.py`).
   - Write `reports/model_card.md` covering intended use, demographic parity, fairness, and model limitations.
   - Write `reports/resume_deliverables.md` containing ATS resume bullet points, LinkedIn project announcement, and 15 deep technical interview Q&As with sample answers.
