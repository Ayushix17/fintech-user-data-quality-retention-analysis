# Fintech User Data Quality and Retention Analysis

Portfolio analytics project using Python, SQL, and Power BI-style reporting to analyze fintech user engagement, transaction quality, and retention patterns across 50,000+ synthetic transaction records.

## Business Objective

The goal is to identify which users, channels, regions, and product categories drive healthy engagement and recurring activity while improving data reliability for downstream reporting.

## Project Highlights

- Generated and analyzed 50,000+ fintech transaction records with realistic data quality issues.
- Cleaned duplicate, invalid, inconsistent, and missing values using Python.
- Built retention cohorts, engagement segments, transaction quality metrics, and KPI summary outputs.
- Created SQL schema and reporting queries for repeatable business analysis.
- Defined Power BI dashboard pages, data model, and DAX measures for executive reporting.

## Folder Structure

```text
data/
  raw/                  Raw generated transaction data
  processed/            Cleaned datasets ready for SQL and BI
outputs/                KPI, cohort, segment, and quality summary CSVs
powerbi/                Dashboard blueprint and DAX measures
scripts/                Python generation and analysis scripts
sql/                    SQLite schema and business queries
```

## How To Run

```powershell
python scripts/generate_data.py
python scripts/analyze_retention.py
```

After running the scripts, import these files into Power BI:

- `data/processed/users_clean.csv`
- `data/processed/transactions_clean.csv`
- `outputs/monthly_kpis.csv`
- `outputs/retention_cohorts.csv`
- `outputs/user_segments.csv`
- `outputs/data_quality_report.csv`

## Core KPIs

- Total transaction volume
- Successful transaction value
- Active users
- Month-over-month active user change
- Repeat user rate
- Failed transaction rate
- Refund rate
- Average transactions per active user
- Monthly cohort retention
- Data quality issue rate

## SQL Usage

The Python analysis script creates `outputs/fintech_retention.db`. You can run the queries in `sql/analysis_queries.sql` against that SQLite database.

## Power BI Deliverable

Use `powerbi/dashboard_blueprint.md` and `powerbi/dax_measures.md` to recreate a dashboard with:

- Executive KPI overview
- Retention cohort heatmap
- Engagement and user segmentation
- Transaction quality monitoring
- Channel, region, and product performance analysis

## Resume Summary

**Fintech User Data Quality Retention Analysis | Python, SQL, Power BI**

- Analyzed 50,000+ user transaction records to identify engagement, retention, and repeat usage patterns.
- Validated and cleaned inconsistent data, including missing values, duplicate records, invalid statuses, negative amounts, and malformed user attributes.
- Built SQL-based KPI and cohort analysis for monthly active users, repeat users, transaction success rate, and failed payment patterns.
- Designed Power BI dashboard logic with executive KPIs, cohort retention views, user segmentation, and data quality monitoring.
