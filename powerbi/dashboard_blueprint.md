# Power BI Dashboard Blueprint

## Data Model

Load these tables:

- `users_clean`
- `transactions_clean`
- `monthly_kpis`
- `retention_cohorts`
- `user_segments`
- `data_quality_report`

Recommended relationships:

- `users_clean[user_id]` 1-to-many `transactions_clean[user_id]`
- `users_clean[user_id]` 1-to-1 `user_segments[user_id]`

Create a date table from `transactions_clean[transaction_date]` and relate it to the transaction date column.

## Page 1: Executive Overview

Visuals:

- KPI cards: Total Transaction Value, Active Users, Success Rate, Failure Rate, Repeat User Rate.
- Line chart: Active users by transaction month.
- Column chart: Successful transaction value by transaction month.
- Bar chart: Total amount by acquisition channel.
- Slicers: Date, region, acquisition channel, device type, transaction type.

## Page 2: Retention Cohorts

Visuals:

- Matrix heatmap: cohort month by months since first transaction, using retention rate.
- Line chart: retention rate by months since first transaction.
- Bar chart: cohort users by cohort month.

## Page 3: User Segmentation

Visuals:

- Donut chart: users by engagement segment.
- Table: top users by total spend, transaction count, and days since last transaction.
- Bar chart: engagement segment by acquisition channel.
- Bar chart: at-risk users by region.

## Page 4: Data Quality Monitoring

Visuals:

- KPI cards: duplicate transaction IDs, invalid amounts, orphan transactions, missing payment methods.
- Table: quality check, severity, affected records, resolution.
- Bar chart: affected records by severity.

## Page 5: Transaction Operations

Visuals:

- Stacked column chart: status by month.
- Bar chart: failure rate by payment method.
- Bar chart: transaction value by transaction type.
- Matrix: device type by payment method with success rate.

## Suggested Formatting

- Use a muted finance palette: navy, teal, green, gray, and amber for warnings.
- Use red only for failed transactions and high-severity data quality checks.
- Keep slicers on the left or top consistently across pages.
- Use conditional formatting in the retention matrix from light gray to green.
