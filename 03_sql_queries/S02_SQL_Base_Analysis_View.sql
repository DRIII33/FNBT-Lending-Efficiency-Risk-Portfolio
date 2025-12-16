-- S02_SQL_Base_Analysis_View.sql
-- Description: Optimized SQL for initial cleaning, transformation, and creating the
-- Loan_Analysis_Base table. This completes the first phase of ETL/Data Preparation.
-- Project ID: driiiportfolio

-----------------------------------------------------------
-- 1. Optimized ETL Query to Create the Base Analysis Table
-- Maps to: Integrate automation, ETL / ELT of data; Review department reports for accuracy.
-----------------------------------------------------------
CREATE OR REPLACE TABLE driiiportfolio.FNBT_Analysis.Loan_Analysis_Base AS
SELECT
    -- Select and TRIM the Region (Data Cleaning)
    t1.Application_ID,
    TRIM(t1.Region) AS Region,
    t1.Applied_Amount,
    t1.Status,
    t1.Date_Submitted,
    t1.Transaction_Flags,

    -- Handling of Risk Score (Data Integrity: Filter out nulls/errors in the WHERE clause)
    t1.Risk_Score_Raw,

    -- Feature Engineering: Create a categorical risk band (Segmentation)
    CASE
        WHEN t1.Risk_Score_Raw IS NULL THEN 'D_Missing_Risk' -- Handle the very few nulls
        WHEN t1.Risk_Score_Raw >= 740 THEN 'A_Low_Risk'
        WHEN t1.Risk_Score_Raw BETWEEN 670 AND 739 THEN 'B_Med_Risk'
        ELSE 'C_High_Risk'
    END AS Risk_Band,

    -- Handling Missing Time-to-Approve (Data Integrity & ETL for 'Pending_Review')
    -- COALESCE replaces NULLs with a known placeholder (999.0) for consistent downstream processing.
    COALESCE(t1.Time_to_Approve_Hrs, 999.0) AS Time_to_Approve_Hrs_Clean,

    -- Extract Day of Week from Timestamp for deeper trend analysis
    FORMAT_TIMESTAMP('%A', t1.Date_Submitted) AS Submission_Day_of_Week

FROM
    -- Use an alias (t1) for cleaner, faster queries
    driiiportfolio.FNBT_Analysis.Loan_Application_Raw AS t1
-- Filter (Prune) the data early to remove records that cannot be used in analysis
WHERE
    t1.Applied_Amount > 100.0 -- Ensure a valid loan amount
    AND t1.Date_Submitted IS NOT NULL; -- Ensure a valid submission time

-- Query Execution Validation Check:
SELECT
    count(1) AS total_records_processed,
    SUM(CASE WHEN Time_to_Approve_Hrs_Clean = 999.0 THEN 1 ELSE 0 END) AS pending_records_count,
    COUNT(DISTINCT Region) AS distinct_regions
FROM
    driiiportfolio.FNBT_Analysis.Loan_Analysis_Base;
