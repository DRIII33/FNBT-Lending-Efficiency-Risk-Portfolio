-- S01_BigQuery_Schema_ETL.sql
-- Description: Creates the BigQuery Dataset and the DDL for the raw data table.
-- Project ID: driiiportfolio

-----------------------------------------------------------
-- 1. Create Dataset (if it doesn't exist)
-- This acts as the database container for the project.
-----------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS driiiportfolio.FNBT_Analysis
OPTIONS(
  location="us"
);

-----------------------------------------------------------
-- 2. Create the Raw Data Table (DDL)
-- The schema definition for the initial load of Loan_Application_Data_Raw.csv.
-- Maps to: Maintain datasets using Oracle / SQL
-----------------------------------------------------------
CREATE OR REPLACE TABLE driiiportfolio.FNBT_Analysis.Loan_Application_Raw (
    Application_ID INT64 NOT NULL,
    Region STRING,
    Risk_Score_Raw INT64,
    Applied_Amount FLOAT64,
    Status STRING,
    Date_Submitted TIMESTAMP,
    Time_to_Approve_Hrs FLOAT64,
    Transaction_Flags STRING,
    Customer_Age INT64
);

-- Note for Execution: After running this script, the user must manually
-- upload the 'Loan_Application_Data_Raw.csv' file into this new table
-- using the BigQuery Web UI or a BigQuery load command.
