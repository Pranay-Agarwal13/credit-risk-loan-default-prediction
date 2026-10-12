-- ==============================================================================
-- Query 01: Default Rate by Categorical Demographic & Loan Dimensions
-- Purpose: Evaluate historical default frequency (TARGET = 1) across key segments:
--          Contract Type, Gender, Education, Family Status, and Housing Type.
-- Engine: DuckDB / SQLite compliant
-- ==============================================================================

-- 1. Default Rate by Loan Contract Type
SELECT 
    NAME_CONTRACT_TYPE AS contract_type,
    COUNT(*) AS total_applicants,
    SUM(TARGET) AS total_defaulters,
    ROUND(AVG(TARGET) * 100, 2) AS default_rate_pct,
    ROUND(AVG(AMT_CREDIT), 2) AS avg_credit_amount,
    ROUND(AVG(AMT_INCOME_TOTAL), 2) AS avg_income
FROM application_train
WHERE TARGET IS NOT NULL
GROUP BY NAME_CONTRACT_TYPE
ORDER BY default_rate_pct DESC;

-- 2. Default Rate by Gender and Family Status
SELECT 
    CODE_GENDER AS gender,
    NAME_FAMILY_STATUS AS family_status,
    COUNT(*) AS total_applicants,
    SUM(TARGET) AS total_defaulters,
    ROUND(AVG(TARGET) * 100, 2) AS default_rate_pct,
    ROUND(AVG(AMT_CREDIT / NULLIF(AMT_INCOME_TOTAL, 0)), 2) AS avg_credit_to_income_ratio
FROM application_train
WHERE TARGET IS NOT NULL AND CODE_GENDER != 'XNA'
GROUP BY CODE_GENDER, NAME_FAMILY_STATUS
HAVING COUNT(*) >= 500
ORDER BY default_rate_pct DESC;

-- 3. Default Rate by Education Type
SELECT 
    NAME_EDUCATION_TYPE AS education_level,
    COUNT(*) AS total_applicants,
    SUM(TARGET) AS total_defaulters,
    ROUND(AVG(TARGET) * 100, 2) AS default_rate_pct,
    ROUND(AVG(AMT_INCOME_TOTAL), 2) AS avg_income,
    ROUND(AVG(AMT_CREDIT), 2) AS avg_credit
FROM application_train
WHERE TARGET IS NOT NULL
GROUP BY NAME_EDUCATION_TYPE
ORDER BY default_rate_pct DESC;

-- 4. Default Rate by Housing Type
SELECT 
    NAME_HOUSING_TYPE AS housing_type,
    COUNT(*) AS total_applicants,
    SUM(TARGET) AS total_defaulters,
    ROUND(AVG(TARGET) * 100, 2) AS default_rate_pct
FROM application_train
WHERE TARGET IS NOT NULL
GROUP BY NAME_HOUSING_TYPE
ORDER BY default_rate_pct DESC;
