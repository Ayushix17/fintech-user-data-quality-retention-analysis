-- 1. Monthly KPI trend
SELECT
    transaction_month,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT user_id) AS active_users,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(SUM(CASE WHEN status = 'Success' THEN amount ELSE 0 END), 2) AS successful_amount,
    ROUND(1.0 * SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) / COUNT(*), 4) AS failed_transaction_rate
FROM transactions
GROUP BY transaction_month
ORDER BY transaction_month;

-- 2. Repeat user rate by month
WITH monthly_user_tx AS (
    SELECT
        transaction_month,
        user_id,
        COUNT(*) AS tx_count
    FROM transactions
    GROUP BY transaction_month, user_id
)
SELECT
    transaction_month,
    COUNT(*) AS active_users,
    SUM(CASE WHEN tx_count >= 2 THEN 1 ELSE 0 END) AS repeat_users,
    ROUND(1.0 * SUM(CASE WHEN tx_count >= 2 THEN 1 ELSE 0 END) / COUNT(*), 4) AS repeat_user_rate
FROM monthly_user_tx
GROUP BY transaction_month
ORDER BY transaction_month;

-- 3. Acquisition channel quality and monetization
SELECT
    u.acquisition_channel,
    COUNT(DISTINCT u.user_id) AS users,
    COUNT(t.transaction_id) AS transactions,
    ROUND(SUM(t.amount), 2) AS total_amount,
    ROUND(AVG(t.amount), 2) AS avg_transaction_amount,
    ROUND(1.0 * SUM(CASE WHEN t.status = 'Success' THEN 1 ELSE 0 END) / COUNT(t.transaction_id), 4) AS success_rate
FROM users u
LEFT JOIN transactions t
    ON u.user_id = t.user_id
GROUP BY u.acquisition_channel
ORDER BY total_amount DESC;

-- 4. Users at risk of churn
SELECT
    user_id,
    region,
    acquisition_channel,
    transaction_count,
    total_spend,
    days_since_last_transaction,
    engagement_segment
FROM user_segments
WHERE engagement_segment = 'At Risk'
ORDER BY total_spend DESC
LIMIT 100;

-- 5. Retention cohort table
SELECT
    cohort_month,
    months_since_first_tx,
    cohort_users,
    active_users,
    retention_rate
FROM retention_cohorts
WHERE months_since_first_tx BETWEEN 0 AND 12
ORDER BY cohort_month, months_since_first_tx;

-- 6. Data quality issue summary
SELECT
    severity,
    COUNT(*) AS checks,
    SUM(affected_records) AS affected_records
FROM data_quality_report
GROUP BY severity
ORDER BY affected_records DESC;
