#INSTALL PACKAGES
pip install pandas google-cloud-bigquery scikit-learn numpy


import pandas as pd
from google.cloud import bigquery
from sklearn.ensemble import IsolationForest
import numpy as np
import os

# --- START: AUTHENTICATION BLOCK FOR GOOGLE COLAB ---
from google.colab import auth

try:
    # Authenticate user credentials and set project ID
    auth.authenticate_user()
    print("Authentication successful.")
except Exception as e:
    print(f"Authentication failed. Please ensure you are running in Colab: {e}")

# Set the BigQuery project ID after authentication
PROJECT_ID = "driiiportfolio"
client = bigquery.Client(project=PROJECT_ID)
# --- END: AUTHENTICATION BLOCK FOR GOOGLE COLAB ---


# Define the target efficiency threshold (24 hours is the business goal)
EFFICIENCY_THRESHOLD = 24.0
# Define the expected anomaly rate (e.g., 1% of transactions are high-risk)
ANOMALY_CONTAMINATION = 0.01

# ----------------------------------------------------------------------
# 2. SQL Query to Fetch Data from the Base Analysis Table
# ----------------------------------------------------------------------
FETCH_QUERY = f"""
SELECT
    Application_ID,
    Region,
    Risk_Score_Raw,
    Applied_Amount,
    Status,
    Date_Submitted,
    Time_to_Approve_Hrs_Clean,
    Transaction_Flags,
    Customer_Age,
    Risk_Band
FROM
    {PROJECT_ID}.FNBT_Analysis.Loan_Analysis_Base
"""

print(f"Fetching data from {PROJECT_ID}.FNBT_Analysis.Loan_Analysis_Base...")
try:
    # Fetch data into a Pandas DataFrame
    df = client.query(FETCH_QUERY).to_dataframe()
    print(f"Successfully fetched {len(df)} rows of data.")
except Exception as e:
    # The error message will now be more informative if authentication failed above.
    print(f"FATAL ERROR: Could not fetch data from BigQuery: {e}")
    df = pd.DataFrame() # Create empty DF to prevent downstream errors

if not df.empty:
    # ----------------------------------------------------------------------
    # 3. Operational Efficiency Flagging
    # Maps to: Perform research and analysis on assigned areas
    # ----------------------------------------------------------------------
    print("\n3. Calculating Operational Efficiency Flags...")

    # We only care about the time for 'Approved' applications to measure efficiency.
    df['Efficiency_Flag'] = np.where(
        df['Status'] == 'Approved',
        np.where(df['Time_to_Approve_Hrs_Clean'] <= EFFICIENCY_THRESHOLD, 'On_Target', 'Needs_Review'),
        'Not_Applicable_Yet'
    )

    # ----------------------------------------------------------------------
    # 4. Compliance Risk Analysis: Unsupervised Anomaly Detection
    # Maps to: Perform research and analysis (BSA/AML Risk)
    # ----------------------------------------------------------------------
    print("4. Running Isolation Forest for Anomaly Detection (BSA Risk)...")

    # Define features for the model: Applied_Amount (size) and Risk_Score_Raw (quality).
    X = df[['Applied_Amount', 'Risk_Score_Raw']].copy()

    # Handle the small number of NaNs introduced in the raw data (use mean imputation for the model)
    X['Risk_Score_Raw'] = X['Risk_Score_Raw'].fillna(X['Risk_Score_Raw'].mean())

    # Initialize and train the Isolation Forest model
    iso_forest = IsolationForest(
        contamination=ANOMALY_CONTAMINATION,
        random_state=42,
        n_estimators=100
    )
    iso_forest.fit(X)

    # Predict anomalies: -1 for anomaly, 1 for inlier
    df['Anomaly_Flag_Model'] = iso_forest.predict(X)

    # ----------------------------------------------------------------------
    # 5. Final Risk Level Aggregation
    # This combines model-based anomalies with pre-existing Transaction_Flags.
    # ----------------------------------------------------------------------

    # Define High Risk based on EITHER the model or an existing Compliance Flag
    df['BSA_Risk_Level'] = np.where(
        (df['Anomaly_Flag_Model'] == -1) | (df['Transaction_Flags'] != 'None'),
        'High_Risk_Anomaly',
        'Low_Risk_Normal'
    )

    # Add a column for ease of filtering in the final report
    df['Is_High_Risk'] = (df['BSA_Risk_Level'] == 'High_Risk_Anomaly').astype(int)

    # ----------------------------------------------------------------------
    # 6. Final Data Preparation and Upload to BigQuery
    # Maps to: Integrate automation, ETL / ELT of data
    # ----------------------------------------------------------------------

    # Select the columns for the final analysis table (as defined in the Data Dictionary)
    df_final = df[[
        'Application_ID', 'Region', 'Risk_Band', 'Applied_Amount', 'Status',
        'Date_Submitted', 'Time_to_Approve_Hrs_Clean', 'Efficiency_Flag',
        'BSA_Risk_Level', 'Customer_Age', 'Is_High_Risk'
    ]].copy()

    # Define the destination table
    table_id = f"{PROJECT_ID}.FNBT_Analysis.Loan_Risk_Results"

    print(f"\n6. Uploading final enriched data to BigQuery table: {table_id}")

    # Upload the final DataFrame to BigQuery, overwriting the table
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

    job = client.load_table_from_dataframe(
        df_final, table_id, job_config=job_config
    )
    job.result()  # Wait for the job to complete

    print(f"\nSUCCESS: Final analysis table created/updated: {table_id}")
    print(f"Total records in final table: {job.output_rows}")

    # ----------------------------------------------------------------------
    # 7. Deliverable: High Risk Application List (CSV Output)
    # ----------------------------------------------------------------------

    high_risk_list = df_final[df_final['BSA_Risk_Level'] == 'High_Risk_Anomaly']

    OUTPUT_FOLDER = '05_deliverables'
    OUTPUT_FILE = 'D01_High_Risk_Application_List.csv'

    # Create the directory if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    high_risk_list.to_csv(f'{OUTPUT_FOLDER}/{OUTPUT_FILE}', index=False)

    print(f"\nSUCCESS: Generated High Risk Application List for Compliance review: {OUTPUT_FILE}")
    print(f"Number of High Risk Applications Flagged: {len(high_risk_list)}")

else:
    print("\nPython analysis skipped due to empty DataFrame (check authentication/BigQuery connection).")
