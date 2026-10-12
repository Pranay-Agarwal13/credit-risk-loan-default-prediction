-- ==============================================================================
-- Query 03: Top 10 Highest-Risk Applicant Segments
-- Purpose: Uncover multi-dimensional cohorts with acute default concentration
--          combining education, employment category, age cohort, and external credit proxy.
-- Engine: DuckDB / SQLite compliant
-- ==============================================================================

WITH segmented_applicants AS (
    SELECT 
        SK_ID_CURR,
        TARGET,
        NAME_EDUCATION_TYPE AS education,
        OCCUPATION_TYPE AS occupation,
        CASE 
            WHEN ABS(DAYS_BIRTH) / 365.25 < 30 THEN 'Under 30'
            WHEN ABS(DAYS_BIRTH) / 365.25 BETWEEN 30 AND 45 THEN '30 to 45'
            WHEN ABS(DAYS_BIRTH) / 365.25 BETWEEN 46 AND 60 THEN '46 to 60'
            ELSE 'Over 60'
        END AS age_cohort,
        CASE 
            WHEN (COALESCE(EXT_SOURCE_2, 0) + COALESCE(EXT_SOURCE_3, 0)) / 2.0 < 0.35 THEN 'Low Ext Score (<0.35)'
            WHEN (COALESCE(EXT_SOURCE_2, 0) + COALESCE(EXT_SOURCE_3, 0)) / 2.0 BETWEEN 0.35 AND 0.60 THEN 'Mid Ext Score (0.35-0.60)'
            ELSE 'High Ext Score (>0.60)'
        END AS external_score_tier,
        CASE 
            WHEN (AMT_CREDIT / NULLIF(AMT_INCOME_TOTAL, 0)) > 5.0 THEN 'High Leverage (>5x)'
            ELSE 'Normal Leverage (<=5x)'
        END AS leverage_tier
    FROM application_train
    WHERE TARGET IS NOT NULL
)
SELECT 
    age_cohort,
    education,
    external_score_tier,
    leverage_tier,
    COUNT(*) AS total_applicants,
    SUM(TARGET) AS total_defaults,
    ROUND(AVG(TARGET) * 100, 2) AS segment_default_rate_pct,
    ROUND(
        (AVG(TARGET) / (SELECT AVG(TARGET) FROM application_train)) * 100, 
        1
    ) AS risk_index_vs_baseline
FROM segmented_applicants
GROUP BY age_cohort, education, external_score_tier, leverage_tier
HAVING COUNT(*) >= 250
ORDER BY segment_default_rate_pct DESC
LIMIT 10;
