#INSTALL PACKAGES
!pip install pandas

# 02_Data_Prep_Synthetic_Data_Generator.ipynb
# Description: Generates 10,000 rows of realistic, synthetic data simulating personal loan applications
# at First National Bank Texas, including transactional flags for risk analysis.
# Maps to: Data Preparation, Data Understanding, and creating the raw dataset.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set the number of rows for the dataset
NUM_APPLICATIONS = 10000
np.random.seed(42) # for reproducibility

# ----------------------------------------------------------------------
# 1. Define Realistic Parameters
# ----------------------------------------------------------------------

# Simulate FNBT service areas
regions = ['Killeen', 'Fort_Hood', 'Waco', 'Temple', 'Round_Rock']
region_probabilities = [0.45, 0.25, 0.15, 0.10, 0.05] # Higher volume in Killeen/Fort Hood area

# Simulate application status based on a rough probability
status_options = ['Approved', 'Denied', 'Pending_Review']
status_probabilities = [0.65, 0.25, 0.10]

# Simulate compliance transaction flags (BSA/AML relevance)
flag_options = ['None'] * 95 + ['High_Velocity_Deposit'] * 3 + ['Suspicious_ACH'] * 2

# Define the start date for data generation (e.g., the last 6 months)
start_date = datetime.now() - timedelta(days=180)
end_date = datetime.now()

# ----------------------------------------------------------------------
# 2. Generate Synthetic Data
# ----------------------------------------------------------------------

data = {}

# Application ID (Unique Identifier)
data['Application_ID'] = range(100000, 100000 + NUM_APPLICATIONS)

# Region (Simulated Geographic Distribution)
data['Region'] = np.random.choice(regions, NUM_APPLICATIONS, p=region_probabilities)

# Risk Score Raw (Normal distribution centered around the typical FICO range)
data['Risk_Score_Raw'] = np.random.normal(loc=700, scale=60, size=NUM_APPLICATIONS).astype(int)
# Cap scores to a reasonable range
data['Risk_Score_Raw'] = np.clip(data['Risk_Score_Raw'], 500, 850)

# Applied Amount (Simulated personal loan amounts, skewed higher for anomalies)
data['Applied_Amount'] = np.random.lognormal(mean=7.5, sigma=0.8, size=NUM_APPLICATIONS)
data['Applied_Amount'] = np.clip(data['Applied_Amount'], 500, 25000).round(2)

# Status (Distribution based on probabilities)
data['Status'] = np.random.choice(status_options, NUM_APPLICATIONS, p=status_probabilities)

# Date Submitted (Realistic time series data)
data['Date_Submitted'] = [
    start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds())))
    for _ in range(NUM_APPLICATIONS)
]

# Customer Age (Realistic age distribution)
data['Customer_Age'] = np.random.randint(22, 65, NUM_APPLICATIONS)

# Transaction Flags (Simulated compliance issues)
data['Transaction_Flags'] = np.random.choice(flag_options, NUM_APPLICATIONS)

# Time to Approve (in hours) - Key Efficiency Metric
# Approved loans have a faster, skewed distribution (mean 12 hrs)
# Denied loans have a slightly slower distribution (mean 36 hrs)
time_to_approve = []
for status in data['Status']:
    if status == 'Approved':
        # Faster approval times, skewed towards low values
        time_to_approve.append(np.random.gamma(shape=2.5, scale=6.0))
    elif status == 'Denied':
        # Moderate time
        time_to_approve.append(np.random.gamma(shape=3.0, scale=12.0))
    else: # Pending_Review (Simulate very long/missing time)
        # Use a high placeholder for pending reviews (to be handled in SQL/Python)
        time_to_approve.append(np.nan) 
data['Time_to_Approve_Hrs'] = np.array(time_to_approve).round(2)


# ----------------------------------------------------------------------
# 3. Create DataFrame and Final Cleanup
# ----------------------------------------------------------------------

df = pd.DataFrame(data)

# Introduce a small percentage of NULLs in Risk Score for realistic data integrity challenge
null_indices = df.sample(frac=0.005, random_state=42).index
df.loc[null_indices, 'Risk_Score_Raw'] = np.nan

# Reorder columns to match the defined Data Dictionary
df = df[[
    'Application_ID', 'Region', 'Risk_Score_Raw', 'Applied_Amount', 'Status', 
    'Date_Submitted', 'Time_to_Approve_Hrs', 'Transaction_Flags', 'Customer_Age'
]]

# ----------------------------------------------------------------------
# 4. Save the Raw Data File
# ----------------------------------------------------------------------

FILE_NAME = 'Loan_Application_Data_Raw.csv'
df.to_csv(FILE_NAME, index=False)
print(f"Successfully generated {len(df)} rows of synthetic data.")
print(f"Data saved to {FILE_NAME} in the current directory.")

# Display a sample of the generated data for immediate review
print("\n--- Sample of Generated Data ---")
print(df.head())
