# AI Model Card: Credit Risk & Loan Default Prediction System

## 1. Model Details
- **Model Name:** Tuned XGBoost Credit Risk Classifier with Cost-Sensitive Thresholding
- **Model Version:** 1.0.0
- **Model Architecture:** Gradient Boosted Decision Trees (`XGBClassifier`) with `scale_pos_weight=11.38`, integrated within an end-to-end scikit-learn `Pipeline` and `ColumnTransformer` (median imputers, robust scalers, one-hot encoders).
- **Interpretability Framework:** TreeSHAP (`shap.TreeExplainer`) for global feature ranking and local applicant waterfall attribution.
- **License:** Apache 2.0 / Educational Open Source

## 2. Intended Use & Target Persona
- **Primary Use:** Decision-support tool for retail credit underwriters, credit risk committees, and portfolio risk managers to score consumer loan default risk.
- **Decision Tier Mapping:**
  - *Low Risk ($p < 0.10$):* Standard prime approval.
  - *Medium Risk ($0.10 \le p < 0.25$):* Automated verification check.
  - *High Risk ($0.25 \le p < 0.50$):* Escalate for senior manual underwriting review.
  - *Critical Risk ($p \ge 0.50$):* Adverse action or secured exception review.
- **Out-of-Scope / Prohibited Uses:**
  - Fully automated, unassisted loan denials without human underwriter concurrence.
  - Using demographic features (gender, family status) as punitive standalone criteria.
  - Sovereign or large corporate credit scoring.

## 3. Training & Evaluation Data
- **Source:** Kaggle Home Credit Default Risk Competition (`application_train.csv` and `bureau.csv`).
- **Target Variable:** `TARGET` (1 = payment difficulties / default, 0 = loan repaid).
- **Training Population:** 246,008 historical loan applications.
- **Held-Out Test Population:** 61,503 unseen applications (20% stratified holdout).
- **Target Imbalance:** 8.07% positive default prevalence (1:11.38 ratio).

## 4. Quantitative Performance Metrics
- **ROC-AUC (Receiver Operating Characteristic):** `0.7782` (Held-out Test) | `0.7795 ± 0.0029` (5-Fold CV)
- **PR-AUC (Precision-Recall Area Under Curve):** `0.2814` (vs 0.0807 random baseline)
- **Selected Operational Threshold:** `0.24` (Optimized on cost curve: $c_{FN}=\$10,000$, $c_{FP}=\$1,200$)
- **Defaulter Recall (@ 0.24 threshold):** `74.18%` (Catches 3,682 of 4,963 test defaulters)
- **Model Precision (@ 0.24 threshold):** `26.45%`
- **Estimated Net Loss Reduction:** `$13.18M` per 61,500 evaluated applicants compared to default 0.50 threshold.

## 5. Ethical Considerations & Fairness Analysis
- **Equal Credit Opportunity Act (ECOA) & FCRA Compliance:** Under ECOA, protected classes must not suffer unlawful disparate impact. While demographic variables exist in the raw research dataset, production deployment should assess Disparate Impact Ratio (DIR) across age and gender.
- **Demographic Parity Assessment:** Male applicants exhibit a baseline default rate of 10.14% vs 6.99% for female applicants. The model’s reliance on objective financial burden metrics (Debt-to-Income, bureau overdue history, external scores) mitigates reliance on demographic indicators.
- **Adverse Action Reason Codes:** The SHAP explainability engine translates top positive log-odds contributors into standardized reason codes (e.g., "High Debt-to-Income Leverage", "Delinquent Prior Bureau Record", "Low External Credit Score") fulfilling regulatory adverse action disclosure requirements.

## 6. Caveats & Limitations
1. **Statistical Association vs Causality:** SHAP values represent model-learned mathematical associations from historical correlations and do not demonstrate causal mechanisms.
2. **Macroeconomic Shifts:** Model was trained on historical consumer credit cycles. Significant interest rate spikes or macro recessions will require feature distribution re-calibration.
3. **Data Drift Monitoring:** Model performance requires ongoing monitoring using Population Stability Index (PSI) and Characteristic Analysis.
