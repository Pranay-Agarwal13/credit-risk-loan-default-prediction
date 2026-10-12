-- ==============================================================================
-- Query 02: Average Income, Credit Amount, Annuity, and Financial Ratios by Target
-- Purpose: Contrast non-defaulters (TARGET = 0) vs defaulters (TARGET = 1) across
--          central tendency, payment burden, and leverage ratios.
-- Engine: DuckDB / SQLite compliant
-- ==============================================================================

SELECT 
    CASE 
        WHEN TARGET = 1 THEN 'Defaulters (Payment Difficulties)'
        ELSE 'Repaid (Non-Defaulters)'
    END AS borrower_status,
    COUNT(*) AS applicant_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM application_train), 2) AS portfolio_share_pct,
    
    -- Income and Loan Size
    ROUND(AVG(AMT_INCOME_TOTAL), 2) AS mean_income,
    ROUND(AVG(AMT_CREDIT), 2) AS mean_credit_amount,
    ROUND(AVG(AMT_ANNUITY), 2) AS mean_annuity,
    ROUND(AVG(AMT_GOODS_PRICE), 2) AS mean_goods_price,
    
    -- Key Underwriting Leverage Ratios
    ROUND(AVG(AMT_CREDIT / NULLIF(AMT_INCOME_TOTAL, 0)), 2) AS mean_credit_to_income_ratio,
    ROUND(AVG(AMT_ANNUITY / NULLIF(AMT_INCOME_TOTAL, 0)) * 100, 2) AS mean_annuity_to_income_pct,
    ROUND(AVG(AMT_ANNUITY / NULLIF(AMT_CREDIT, 0)) * 100, 2) AS mean_payment_rate_pct,
    
    -- External Credit Bureau Scoring Indicators
    ROUND(AVG(EXT_SOURCE_1), 4) AS mean_ext_source_1,
    ROUND(AVG(EXT_SOURCE_2), 4) AS mean_ext_source_2,
    ROUND(AVG(EXT_SOURCE_3), 4) AS mean_ext_source_3,
    
    -- Age and Employment Tenure
    ROUND(AVG(ABS(DAYS_BIRTH) / 365.25), 1) AS mean_age_years,
    ROUND(AVG(CASE WHEN DAYS_EMPLOYED < 0 THEN ABS(DAYS_EMPLOYED) / 365.25 ELSE 0 END), 1) AS mean_employed_years
FROM application_train
WHERE TARGET IS NOT NULL
GROUP BY TARGET;
