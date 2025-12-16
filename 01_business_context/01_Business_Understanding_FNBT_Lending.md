# 01_Business_Understanding_FNBT_Lending

## Project Scope and Business Context

### A. The Business Imperative: Lending Efficiency and Compliance

First National Bank Texas (FNBT), like many regional banks, faces growing pressure from two critical areas: competitive speed and regulatory compliance. The Data Analyst role is tasked with improving operational efficiency while simultaneously building robust data systems to meet increasing scrutiny from bodies like the OCC regarding risk (e.g., BSA/AML).

**Key Business Goals Addressed:**
1.  **Operational Efficiency:** Reduce the **Time-to-Approve** for personal loan applications to enhance customer experience and capture market share from faster competitors.
2.  **Regulatory Risk Mitigation:** Proactively identify and flag high-risk or anomalous transactions before they lead to regulatory non-compliance or financial loss.

### B. Business Problem Statement

> "Current reliance on manual data aggregation and review processes for personal loans results in approval times significantly exceeding our competitive target of **24 hours**. This delay, coupled with fragmented data across systems, hinders our ability to generate timely and comprehensive reports necessary for effective compliance monitoring (BSA/AML)."

### C. The Solution Framework: CRISP-DM

We are adopting the **Cross-Industry Standard Process for Data Mining (CRISP-DM)** to ensure a structured, repeatable, and easily auditable approach to this problem. 

| CRISP-DM Stage | Project Action | Project Deliverable(s) |
| :--- | :--- | :--- |
| **1. Business Understanding** | Define the 24-hour efficiency target and the BSA/AML risk objectives. | `01_Business_Understanding_FNBT_Lending.pdf` |
| **2. Data Understanding** | Define required fields (e.g., Risk Score, Applied Amount, Approval Time) and assess data quality needs. | `00_Data_Dictionary.csv` |
| **3. Data Preparation** | **SQL ETL/ELT:** Clean, transform, and standardize raw data; handle missing values (`Time_to_Approve_Hrs_Clean`). | `S02_SQL_Base_Analysis_View.sql` |
| **4. Modeling** | **Python Analysis:** Calculate the binary **Efficiency Flag** and apply the unsupervised **Isolation Forest** model for anomaly detection. | `P01_Loan_Risk_Analysis_Python.ipynb` |
| **5. Evaluation** | Validate the model's accuracy and ensure the outputs are actionable and stable. | Internal checks within Python code; stakeholder feedback. |
| **6. Deployment** | Deliver a dynamic dashboard and prioritized list of action items for departmental use. | `D01_High_Risk_Application_List.csv` & `D02_Executive_Summary_Lending_Report.pdf` (Mockup) |

---
