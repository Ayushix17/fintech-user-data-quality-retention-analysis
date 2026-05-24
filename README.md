# Fintech User Data Quality and Retention Analysis

An end-to-end data analytics portfolio project using **Python, SQL, and Power BI** to analyze fintech user engagement, transaction quality, and customer retention patterns across **50,000+ transaction records**.

The project simulates a real fintech reporting workflow where raw user and transaction data must be validated, cleaned, modeled, analyzed, and presented through an executive dashboard.

## Business Objective

Fintech platforms depend on reliable transaction data and repeat user activity. This project answers four business questions:

- Which users and acquisition channels drive engagement?
- How strong is user retention after the first transaction?
- Which transaction types, devices, and payment methods perform best?
- What data quality issues could affect reporting accuracy?

## Executive Summary

- Analyzed **52,340 raw transaction records** and **12,000 user records**.
- Cleaned the dataset down to **51,700 valid transactions** after removing or correcting quality issues.
- Measured **7.41M total transaction value** across the cleaned dataset.
- Identified **11,853 active users** and **11,127 repeat users**.
- Found an overall **success rate of 83.71%** and **failure rate of 8.25%**.
- Built cohort retention analysis showing month-0 retention at **100%**, with later-month retention averaging around **13-17%**.
- Segmented users into **Power User, Engaged, Occasional, At Risk, and No Activity** groups.

## Dashboard Preview

The Power BI dashboard contains five reporting pages:

1. **Executive Overview** - high-level KPIs, monthly trends, channel performance, and slicers.
2. **Retention Cohorts** - cohort heatmap and retention trend by months since first transaction.
3. **User Segments** - engagement segmentation and at-risk user detail.
4. **Data Quality** - duplicate, invalid, missing, and orphan record monitoring.
5. **Transaction Operations** - transaction status, failure rate, transaction type value, and success-rate matrix.
   
<img width="490" height="290" alt="image" src="https://github.com/user-attachments/assets/79113164-638e-4056-bb53-20cb70537cb3" /><figcaption align="center"><b>Figure 1:</b> Executive overview </figcaption>

<img width="504" height="330" alt="image" src="https://github.com/user-attachments/assets/61bd13ed-9434-4793-8597-863d36d8760c" /><figcaption align="center"><b>Figure 2:</b> Retention Cohorts</figcaption>

<img width="506" height="284" alt="User-segments" src="https://github.com/user-attachments/assets/973c764a-b390-4d7d-84a7-e8762e1c7811" /><figcaption align="center"><b>Figure 3:</b> User Segments</figcaption>

<img width="508" height="285" alt="Data-Quality" src="https://github.com/user-attachments/assets/a1222e38-ad2a-4759-a442-02bbe5501e1d" /><figcaption align="center"><b>Figure 4:</b> Data Quality</figcaption>

<img width="1016" height="570" alt="Transaction-Operations" src="https://github.com/user-attachments/assets/039fc213-85b6-44e1-8500-56be88e603fe" /><figcaption align="center"><b>Figure 5:</b> Transaction Operations</figcaption>

## Key Insights

- **Organic acquisition generated the highest transaction value**, followed by paid search and referral channels.
- **P2P Transfer and Wallet Load** were the strongest transaction categories by total transaction value.
- **At-risk users represented a large segment**, indicating an opportunity for reactivation campaigns.
- **Unknown payment method had the highest failure rate**, suggesting missing payment metadata may be linked to operational issues.
- **Retention dropped sharply after the first transaction month**, making early lifecycle engagement a critical business priority.
- Data quality issues such as duplicate transaction IDs, invalid amounts, and orphan transactions could materially distort KPI reporting if not handled.

## Data Quality Checks

| Data Quality Check | Records Affected | Action Taken |
|---|---:|---|
| Duplicate transaction IDs | 260 | Kept first valid transaction record |
| Invalid or non-positive transaction amounts | 302 | Removed from cleaned transaction table |
| Missing payment method | 180 | Imputed as `Unknown` |
| Transactions without matching user | 80 | Removed from cleaned transaction table |
| Invalid user age | 80 | Replaced with median valid age |

## Business Recommendations

- Launch targeted reactivation campaigns for users in the **At Risk** segment.
- Investigate payment failures by **payment method** and **device type**, especially where payment method is missing or unknown.
- Add upstream validation for transaction ID uniqueness, positive transaction amounts, and valid user references.
- Monitor retention by acquisition channel to identify which channels bring higher-quality users.
- Use monthly KPI reporting to track active users, repeat users, failure rate, and transaction value trends.

## Tools and Skills Demonstrated

- **Python:** data generation, cleaning, validation, feature engineering, cohort analysis.
- **Pandas and NumPy:** data transformation, aggregation, segmentation, and quality checks.
- **SQL / SQLite:** relational schema, KPI queries, retention queries, and reporting tables.
- **Power BI:** data modeling, DAX measures, KPI cards, slicers, matrix heatmaps, and dashboard design.
- **Data Analysis:** user retention, engagement segmentation, data quality monitoring, and business recommendations.

## Project Structure

```text
data/
  raw/                  Raw generated user and transaction data
  processed/            Cleaned datasets ready for SQL and Power BI
outputs/                KPI, cohort, segment, quality, and SQLite outputs
powerbi/                Dashboard blueprint and DAX measure definitions
scripts/                Python data generation and analysis scripts
sql/                    SQL schema and business analysis queries
```

## How To Run

Install dependencies:

```powershell
pip install -r requirements.txt
```

Generate raw synthetic data:

```powershell
python scripts/generate_data.py
```

Run cleaning, analysis, and SQLite export:

```powershell
python scripts/analyze_retention.py
```

## Power BI Setup

Import these files into Power BI:

- `data/processed/users_clean.csv`
- `data/processed/transactions_clean.csv`
- `outputs/monthly_kpis.csv`
- `outputs/retention_cohorts.csv`
- `outputs/user_segments.csv`
- `outputs/data_quality_report.csv`

Use these supporting files:

- `powerbi/dashboard_blueprint.md`
- `powerbi/dax_measures.md`
- `Fintech_User_Data_Quality_Retention_Analysis.pbix`

## SQL Analysis

The analysis script creates:

```text
outputs/fintech_retention.db
```

Run the queries in:

```text
sql/analysis_queries.sql
```

Example analyses included:

- Monthly active users and transaction value
- Repeat user rate by month
- Acquisition channel performance
- At-risk user identification
- Retention cohort reporting
- Data quality issue summary

## Resume Summary

**Fintech User Data Quality and Retention Analysis | Python, SQL, Power BI**

- Analyzed **50,000+ fintech transaction records** to identify user engagement, repeat usage, transaction performance, and retention patterns.
- Cleaned inconsistent data by handling duplicate transaction IDs, invalid transaction amounts, missing payment methods, orphan user references, and invalid user attributes.
- Built SQL-based KPI and cohort reporting for active users, repeat users, transaction success rate, failure rate, and monthly retention.
- Designed a multi-page Power BI dashboard covering executive KPIs, retention cohorts, user segmentation, data quality monitoring, and transaction operations.
- Delivered business recommendations to improve retention strategy, payment reliability, and reporting accuracy.
