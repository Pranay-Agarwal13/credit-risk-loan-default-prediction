-- ==============================================================================
-- Query 04: Distribution of Applicants and Defaults Across Income & Credit Bands
-- Purpose: 2D Matrix of applicant volume, total funded credit, and default risk
--          grouped into standard credit risk exposure bands.
-- Engine: DuckDB / SQLite compliant
-- ==============================================================================

WITH banded_data AS (
    SELECT 
        SK_ID_CURR,
        TARGET,
        AMT_CREDIT,
        AMT_INCOME_TOTAL,
        CASE 
            WHEN AMT_INCOME_TOTAL < 100000 THEN '1. Low (< $100k)'
            WHEN AMT_INCOME_TOTAL BETWEEN 100000 AND 175000 THEN '2. Lower-Mid ($100k-$175k)'
            WHEN AMT_INCOME_TOTAL BETWEEN 175001 AND 275000 THEN '3. Upper-Mid ($175k-$275k)'
            ELSE '4. High (> $275k)'
        END AS income_band,
        CASE 
            WHEN AMT_CREDIT < 250000 THEN 'A. Micro (< $250k)'
            WHEN AMT_CREDIT BETWEEN 250000 AND 600000 THEN 'B. Standard ($250k-$600k)'
            WHEN AMT_CREDIT BETWEEN 600001 AND 1200000 THEN 'C. Large ($600k-$1.2M)'
            ELSE 'D. Jumbo (> $1.2M)'
        END AS credit_band
    FROM application_train
    WHERE TARGET IS NOT NULL
)
SELECT 
    income_band,
    credit_band,
    COUNT(*) AS total_applicants,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_portfolio,
    SUM(TARGET) AS defaulter_count,
    ROUND(AVG(TARGET) * 100, 2) AS default_rate_pct,
    ROUND(SUM(AMT_CREDIT) / 1000000.0, 2) AS total_exposure_millions,
    ROUND(AVG(AMT_CREDIT / NULLIF(AMT_INCOME_TOTAL, 0)), 2) AS avg_debt_to_income
FROM banded_data
GROUP BY income_band, credit_band
ORDER BY income_band, credit_band;
