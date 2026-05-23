# Power BI DAX Measures

Create these measures after importing the cleaned CSV files.

```DAX
Total Transactions = COUNTROWS(transactions_clean)

Successful Transactions =
CALCULATE(
    COUNTROWS(transactions_clean),
    transactions_clean[status] = "Success"
)

Failed Transactions =
CALCULATE(
    COUNTROWS(transactions_clean),
    transactions_clean[status] = "Failed"
)

Total Transaction Value = SUM(transactions_clean[amount])

Successful Transaction Value =
CALCULATE(
    SUM(transactions_clean[amount]),
    transactions_clean[status] = "Success"
)

Active Users = DISTINCTCOUNT(transactions_clean[user_id])

Average Transaction Amount = AVERAGE(transactions_clean[amount])

Transactions Per Active User =
DIVIDE([Total Transactions], [Active Users])

Failure Rate =
DIVIDE([Failed Transactions], [Total Transactions])

Success Rate =
DIVIDE([Successful Transactions], [Total Transactions])

Repeat Users =
COUNTROWS(
    FILTER(
        VALUES(transactions_clean[user_id]),
        CALCULATE(COUNTROWS(transactions_clean)) >= 2
    )
)

Repeat User Rate =
DIVIDE([Repeat Users], [Active Users])

Refunded Transactions =
CALCULATE(
    COUNTROWS(transactions_clean),
    transactions_clean[status] = "Refunded"
)

Refund Rate =
DIVIDE([Refunded Transactions], [Total Transactions])

Data Quality Affected Records =
SUM(data_quality_report[affected_records])

Cohort Retention Rate =
AVERAGE(retention_cohorts[retention_rate])
```
