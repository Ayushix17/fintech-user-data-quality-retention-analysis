# Insights Summary

## Dataset Quality

- Raw input contained 12,000 user records and 52,340 transaction rows.
- Cleaning produced 12,000 user records and 51,700 valid transaction records.
- Key quality issues found:
  - 260 duplicate transaction IDs.
  - 302 invalid or non-positive transaction amounts.
  - 180 missing payment methods.
  - 80 transactions without a matching user.
  - 80 invalid user ages.

## Engagement and Retention

- 11,853 users completed at least one valid transaction.
- 11,127 users made two or more transactions, indicating strong repeat usage in the sample.
- Engagement segmentation:
  - Occasional: 4,730 users.
  - At Risk: 4,427 users.
  - Engaged: 2,628 users.
  - Power User: 68 users.
  - No Activity: 147 users.

## Transaction Performance

- Total cleaned transaction value: 7,407,436.69.
- Overall success rate: 83.71%.
- Overall failure rate: 8.25%.
- March 2023 had the highest monthly active users in the sample, with 1,848 active users.

## Business Interpretation

- The high number of repeat users suggests healthy product stickiness, but the large at-risk segment should be monitored with reactivation campaigns.
- Failed transactions should be analyzed by payment method and device type to identify operational friction.
- Data quality controls should be placed upstream for transaction IDs, amount validation, valid user references, and payment method capture.
