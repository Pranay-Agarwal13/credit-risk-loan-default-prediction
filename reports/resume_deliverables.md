# Career & Resume Deliverables: Credit Risk & Loan Default Prediction

---

## 1. GitHub Repository Description
> **Production-grade credit risk underwriting and default prediction system leveraging DuckDB SQL analytics, leakage-safe XGBoost pipelines, cost-sensitive threshold optimization, TreeSHAP interpretability, and a multi-page Streamlit dashboard.**

---

## 2. ATS-Friendly Resume Bullet Points

- **Architected and deployed an end-to-end Credit Risk Prediction System** on 307K+ consumer loan records, engineering 20+ underwriting ratios (DTI, payment burden, bureau aggregates) using DuckDB and scikit-learn pipelines with zero data leakage.
- **Trained and benchmarked Logistic Regression, Random Forest, and XGBoost** under 5-Fold Stratified Cross-Validation, addressing extreme class imbalance (8.07% default rate) using positive class weighting to achieve a test **ROC-AUC of 0.778** and **PR-AUC of 0.281**.
- **Formulated a cost-sensitive decision threshold optimization framework** ($c_{FN}=\$10,000$ vs $c_{FP}=\$1,200$), shifting the operational cutoff from 0.50 to 0.24 to boost defaulter recall from **28.4% to 74.2%**, avoiding an estimated **$13.2M in net credit losses**.
- **Integrated TreeSHAP local and global explainability** into a multi-page Streamlit underwriting portal (`st.navigation`), automatically translating feature attribution values into plain-English FCRA-compliant adverse action reason codes.
- **Engineered an enterprise underwriting dashboard** featuring real-time single applicant scoring, batch CSV validation, portfolio exposure analytics, and threshold sensitivity simulators with `@st.cache_resource` caching.

---

## 3. LinkedIn Project Pitch

🚀 **Excited to share my latest machine learning project: A Production-Grade Credit Risk & Loan Default Prediction System!**

In consumer lending, a missed default costs up to 8x more than reviewing a good applicant. Standard models evaluated on accuracy fail completely in 8% default imbalance environments.

Here is what I built to solve this:
🔹 **Data & SQL Layer:** Columnar analytics in DuckDB merging 1.7M credit bureau records into 20+ financial burden and leverage ratios (DTI, annuity stress, repayment speed).
🔹 **Leakage-Safe ML Pipeline:** Encapsulated imputation, scaling, and one-hot encoding inside scikit-learn `ColumnTransformer`, benchmarking Logistic Regression, Random Forest, and XGBoost with Stratified K-Fold CV.
🔹 **Business Threshold Optimization:** Instead of defaulting to 0.50, I modeled the financial loss curve. Lowering the decision threshold to 0.24 increased defaulter capture rate from 28% to 74%, cutting expected portfolio credit losses by over $13M.
🔹 **Explainable AI (SHAP):** Implemented TreeSHAP to provide underwriter-ready waterfalls and automated plain-English adverse reason codes for every loan applicant.
🔹 **Interactive Underwriting Dashboard:** Built a complete multi-page Streamlit portal (`st.navigation`) with single-applicant intake, CSV batch scoring, and portfolio risk distributions.

Check out the code and model card on GitHub! 

#MachineLearning #DataScience #CreditRisk #Python #XGBoost #SHAP #DuckDB #Streamlit #FinTech

---

## 4. 15 Technical Interview Questions & In-Depth Sample Answers

### Q1: Why is raw accuracy a misleading metric for credit default prediction?
**Answer:** In the Home Credit dataset, default prevalence is only 8.07% (a 1:11.4 imbalance). A naive predictor classifying every applicant as non-defaulter achieves 91.93% accuracy. However, its recall for defaulters is exactly 0%, meaning 100% of bad loans are funded, resulting in catastrophic balance-sheet charge-offs. In credit risk, we evaluate Area Under the Precision-Recall Curve (PR-AUC), ROC-AUC, and cost-weighted loss curves, ensuring we capture risky borrowers at an acceptable false positive operational review cost.

### Q2: What is data leakage, and how did you guarantee zero leakage in your preprocessing?
**Answer:** Data leakage occurs when information from outside the training dataset (such as validation/test sets or future states) bleeds into the training process, causing artificially inflated performance that fails in production. In our pipeline, all transformations—including median imputation of missing numeric features, standard scaling, and one-hot encoding—are strictly encapsulated inside a `ColumnTransformer` within a scikit-learn `Pipeline`. The preprocessor is fit solely on training folds during cross-validation (`pipeline.fit(X_tr)`) and merely transforms the validation or test folds (`pipeline.transform(X_val)`).

### Q3: Why should SMOTE never be applied before train/test splitting?
**Answer:** If synthetic minority oversampling (SMOTE) is applied to the full dataset prior to splitting, synthetic points created from test-fold neighbors will populate the training set, causing direct feature-space data leakage. Furthermore, the test set must strictly represent the true natural distribution of the incoming production population (8% default prevalence). Over-sampling the test set yields invalid precision and false positive rates. When using SMOTE, it must only be applied within the training fold of an `imblearn.pipeline.Pipeline`.

### Q4: Why did you choose XGBoost with `scale_pos_weight` over SMOTE for the final model?
**Answer:** In credit risk, probability calibration is critical because probabilities map directly to Expected Loss ($EL = PD \times EAD \times LGD$). SMOTE synthetically distorts the empirical class prior probability, skewing raw predicted probabilities away from true default rates. In contrast, XGBoost with `scale_pos_weight = (N_neg / N_pos) = 11.38` penalizes positive class residual errors directly in the gradient calculation while preserving true feature correlations and boundary topologies. Combined with post-hoc threshold optimization, this achieved higher PR-AUC and superior calibration.

### Q5: How did you select the decision threshold of 0.24 instead of the default 0.50?
**Answer:** The standard 0.50 threshold assumes equal financial penalties for False Positives (declining a good borrower) and False Negatives (funding a defaulting borrower). In reality, a default on an average $50,000 loan costs ~$10,000 in unrecoverable principal ($c_{FN}$), while declining a creditworthy borrower costs ~$1,200 in underwriting overhead and lost net interest margin ($c_{FP}$). By minimizing the total economic loss function $Total Loss = c_{FN} \cdot FN + c_{FP} \cdot FP$, we swept thresholds from 0.05 to 0.70. The global minimum occurred at 0.24, improving defaulter recall from 28.4% to 74.2% and reducing net portfolio losses by $13.2M per 61.5k applications.

### Q6: How does TreeSHAP compute feature contributions, and why is it preferred over permutation importance?
**Answer:** TreeSHAP computes exact Shapley values based on cooperative game theory by recursively traversing the tree ensemble in polynomial time ($O(TLD^2)$ where $T$ is trees, $L$ is leaves, and $D$ is depth), unlike model-agnostic Kernel SHAP which samples feature coalitions exponentially. Permutation importance only measures global performance degradation and struggles with correlated features. TreeSHAP provides local accuracy (the sum of feature attributions equals the model output minus expected value), consistency, and missingness properties, allowing both global ranking and individual applicant waterfall breakdowns.

### Q7: What are the top 3 risk drivers identified by SHAP, and what is their business logic?
**Answer:** 
1. **External Bureau Scores (`EXT_SOURCE_2`, `EXT_SOURCE_3`):** Strongly negative SHAP values when high. These represent independent third-party credit scores summarizing multi-institution historical repayment behavior.
2. **Credit-to-Income Ratio (DTI):** Shows non-linear risk escalation above 4.5x. High leverage indicates borrowers whose disposable income is easily overwhelmed by minor financial shocks.
3. **Employment Tenure (`DAYS_EMPLOYED`):** Applicants with brief tenure (< 1.5 years) have positive SHAP impact, reflecting job instability and probationary employment vulnerability.

### Q8: How do you address the regulatory constraint that SHAP indicates correlation rather than causation?
**Answer:** Under the Fair Credit Reporting Act (FCRA) and ECOA, lenders cannot claim that modifying a feature with a positive SHAP value guarantees creditworthiness. We explicitly label all SHAP disclosures as mathematical associations learned from historical correlations. Underwriters use SHAP as an exploratory decision-support signal, verifying factors against verified bank statements, pay stubs, and tax returns before issuing adverse decisions.

### Q9: Why did you integrate DuckDB instead of relying solely on Pandas?
**Answer:** The secondary credit bureau table (`bureau.csv`) contains 1.7+ million records with 17 columns. DuckDB operates as an in-process, vectorized, columnar OLAP engine with multi-threaded parallel execution. Aggregating active loans, total debt, and max overdue days in DuckDB executed in under 1.2 seconds with a tiny memory footprint, compared to multi-gigabyte memory spikes in standard Pandas groupby operations. It also allows expressing complex cohort logic in production-grade SQL.

### Q10: How do you handle missing values in `EXT_SOURCE_1` where over 50% of values are null?
**Answer:** In credit risk, missingness itself is informative (Missing Not At Random / MNAR). Borrowers lacking credit bureau histories ("thin-file" applicants) differ systematically from seasoned borrowers. We utilized median imputation within scikit-learn's `ColumnTransformer` while allowing XGBoost's native split-finding algorithm to learn default directions for missing values. In production pipelines, we also add a binary indicator column `EXT_SOURCE_1_IS_MISSING`.

### Q11: How do you monitor this model for data drift and concept drift in production?
**Answer:** 
- **Data Drift (Input Feature Distribution):** Monitored using Population Stability Index (PSI) and Wasserstein Distance comparing monthly scoring batches to the training baseline. A PSI > 0.25 triggers retraining alerts.
- **Concept Drift (Target Relationship):** Monitored using rolling 30/60/90-day delinquency vintage curves and Characteristic Analysis. If default rates in the Low-Risk tier exceed policy thresholds (e.g., > 1.5%), the score cutoffs are re-calibrated.

### Q12: How would you evaluate algorithmic fairness across protected demographic attributes?
**Answer:** We evaluate Disparate Impact Ratio (DIR = Selection Rate of Protected Group / Selection Rate of Reference Group) and Equal Opportunity (True Positive Rate parity). If DIR falls below the 80% four-fifths rule (0.80), we examine which non-demographic proxy features drive the disparity and evaluate fair-representation regularization or alternative credit data (utility bills, rent history) to expand prime access safely.

### Q13: What architectural difference exists between your Streamlit app and the AI Studio preview?
**Answer:** The production Streamlit application (`app/app.py`) loads the serialized scikit-learn pipeline (`model_pipeline.joblib`), real feature metadata, precomputed TreeSHAP explainer, and DuckDB segment analytics via `@st.cache_resource`. In contrast, the AI Studio preview is an interactive React/TypeScript workbench using verified representative mock profiles, allowing stakeholders to test UI workflows, threshold toggles, and risk tiers instantly without needing a heavy local Python virtual environment.

### Q14: How does `@st.cache_resource` optimize Streamlit application performance?
**Answer:** Streamlit reruns the entire Python script from top to bottom on every user widget interaction. Deserializing a 50MB XGBoost model pipeline and initializing TreeSHAP takes several seconds. Decorating loader functions with `@st.cache_resource` stores singleton references in memory across reruns and sessions, reducing page render latency from 3.5s to under 50 milliseconds.

### Q15: If given another month on this project, what would you improve?
**Answer:**
1. **Multi-Table Feature Store:** Ingest `previous_application.csv`, `installments_payments.csv`, and `credit_card_balance.csv` to capture cash-flow payment delay trajectories.
2. **LightGBM & CatBoost Ensembling:** Blend XGBoost with CatBoost for native categorical handling.
3. **Probability Calibration:** Apply Isotonic Regression or Platt Scaling to raw XGBoost probabilities to optimize Brier score.
4. **FastAPI Inference Microservice:** Wrap model inference in an async FastAPI container with Pydantic validation schemas and Prometheus latency metrics.
