## 📄 `00_README.md`

```markdown
# FNBT-Lending-Efficiency-Risk-Portfolio

## 🏦 Project Title: FNBT Retail Banking Efficiency & Compliance Risk Analysis

### Project Overview
This end-to-end data analysis project is designed to address a critical operational and compliance challenge faced by regional banks, specifically targeting the data analyst role at First National Bank Texas (FNBT) in Killeen, TX. The project demonstrates proficiency in **SQL (ETL/ELT)**, **Python (Modeling/Automation)**, and **Data Visualization** to deliver actionable insights to both Retail Lending and Compliance stakeholders.

### Problem Statement
First National Bank Texas seeks to **reduce the turnaround time for personal loan applications** to improve customer satisfaction and competitive standing, while simultaneously strengthening its reporting on **high-risk transactions** to ensure adherence to stringent BSA/AML regulations. Current manual data aggregation and monitoring processes are contributing to slow approvals and increased regulatory risk.

### Solution: Data-Driven Process Optimization
We developed an automated data pipeline and reporting framework using the **CRISP-DM** (Cross-Industry Standard Process for Data Mining) methodology to transition the bank from reactive reporting to proactive risk and efficiency management.

### Technical Stack & Tools

| Tool/Technology | Purpose in Project | Mapping to FNBT Job Requirement |
| :--- | :--- | :--- |
| **Google BigQuery / SQL** | Data warehousing, defining schema, initial cleaning, and performing optimized ETL/ELT transformations. | **Maintain datasets using Oracle / SQL.** |
| **Python (Pandas, Scikit-learn)** | Data generation, advanced feature engineering, calculating efficiency flags, and unsupervised anomaly (risk) detection (Isolation Forest). | **Integrate automation, ETL / ELT of data.** |
| **Google Colab** | Execution environment for Python automation and modeling. | *General automation/analytical skill.* |
| **Looker Studio (Mockup)** | Final visualization and dashboard creation for stakeholders. | **Create, maintain, and distribute assigned department reporting.** |
| **GitHub** | Version control, documentation, and project distribution. | *Professional standard for analytical work.* |

---

## ⚙️ CRISP-DM Framework & Key Findings

### 1. Business Understanding
**Goal:** Reduce average loan approval time below a 24-hour target and identify high-risk applications immediately.

### 2. Data Understanding & Preparation (See `02_data_preparation/`)
* **Source:** 10,000 rows of custom-generated synthetic data simulating personal loan applications, including raw credit scores, applied amounts, and compliance-related transaction flags.
* **Action:** Generated synthetic data using Python to introduce realistic noise, missing values, and anomalies, simulating real-world data challenges.

### 3. Data Preparation & ETL/ELT (See `03_sql_queries/`)
* **Action:** Used BigQuery SQL (`S02_SQL_Base_Analysis_View.sql`) to clean data, handle nulls, standardize fields, and create a `Risk_Band` categorical feature.
* **Result:** A clean, base table (`Loan_Analysis_Base`) ready for advanced analysis.

### 4. Modeling & Analysis (See `04_analysis_notebooks/`)
* **Action:** Python was used to apply two primary models:
    1.  **Efficiency Flagging:** Created an **`Efficiency_Flag`** (`On_Target` vs. `Needs_Review`) based on the 24-hour approval threshold.
    2.  **Compliance Risk Scoring:** Implemented an **Isolation Forest (Unsupervised ML)** algorithm on `Applied_Amount` and `Risk_Score_Raw` to flag outlier transactions, resulting in a **`BSA_Risk_Level`** column.
* **Result:** The final table (`Loan_Risk_Results`) is generated, containing all core metrics and risk assessments.

### 5. Evaluation & Deployment (See `05_deliverables/`)

| Deliverable | Key Insight/Metric | Stakeholder Value |
| :--- | :--- | :--- |
| **Lending Efficiency Dashboard** (Mockup PDF) | Average Time-to-Approve by Region. Percentage of loans falling into the `Needs_Review` category. | **Retail Lending:** Pinpoints regional/process bottlenecks for targeted optimization efforts. |
| **High Risk Application List** (CSV) | List of applications flagged as `High_Risk_Anomaly`. | **Compliance/BSA:** Provides a prioritized, auditable list of accounts requiring immediate human review, reducing regulatory exposure. |

---

## 📂 Repository Structure

The project follows a modular, phase-based structure for clarity and navigation:

```

FNBT-Lending-Efficiency-Risk-Portfolio/
│
├── 00\_README.md                                \# Project summary and findings (this file).
├── 00\_Data\_Dictionary.csv                      \# Definitions of all synthetic data columns.
│
├── 01\_business\_context/
│   └── 01\_Business\_Understanding\_FNBT\_Lending.pdf \# Context and CRISP-DM framework.
│
├── 02\_data\_preparation/
│   ├── Loan\_Application\_Data\_Raw.csv           \# The raw, generated synthetic dataset.
│   └── 02\_Data\_Prep\_Synthetic\_Data\_Generator.ipynb \# Python code to generate the raw data.
│
├── 03\_sql\_queries/
│   ├── S01\_BigQuery\_Schema\_ETL.sql             \# SQL: Create BigQuery dataset and raw table DDL.
│   └── S02\_SQL\_Base\_Analysis\_View.sql          \# Optimized SQL: Initial cleaning and creating the Loan\_Analysis\_Base table.
│
├── 04\_analysis\_notebooks/
│   └── P01\_Loan\_Risk\_Analysis\_Python.ipynb     \# Python: Anomaly detection, efficiency calculation, and final table upload.
│
└── 05\_deliverables/
├── D01\_High\_Risk\_Application\_List.csv      \# Output: List of flagged high-risk applications.
└── D02\_Executive\_Summary\_Lending\_Report.pdf  \# Output: Mockup of the Looker Studio Dashboard/Report.

```
