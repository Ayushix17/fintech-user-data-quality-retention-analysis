from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "outputs"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.title()


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame]:
    users_path = RAW_DIR / "users_raw.csv"
    transactions_path = RAW_DIR / "transactions_raw.csv"

    if not users_path.exists() or not transactions_path.exists():
        raise FileNotFoundError("Raw files missing. Run scripts/generate_data.py first.")

    users = pd.read_csv(users_path, parse_dates=["signup_date"])
    transactions = pd.read_csv(transactions_path, parse_dates=["transaction_date"])
    return users, transactions


def build_quality_report(users_raw: pd.DataFrame, tx_raw: pd.DataFrame, users: pd.DataFrame, tx: pd.DataFrame) -> pd.DataFrame:
    report = [
        {
            "check_name": "Raw user records",
            "affected_records": len(users_raw),
            "severity": "Info",
            "resolution": "Baseline record count",
        },
        {
            "check_name": "Raw transaction records",
            "affected_records": len(tx_raw),
            "severity": "Info",
            "resolution": "Baseline record count",
        },
        {
            "check_name": "Duplicate transaction IDs",
            "affected_records": int(tx_raw.duplicated("transaction_id").sum()),
            "severity": "High",
            "resolution": "Kept the first transaction_id occurrence",
        },
        {
            "check_name": "Invalid or non-positive transaction amount",
            "affected_records": int((tx_raw["amount"] <= 0).sum()),
            "severity": "High",
            "resolution": "Removed from cleaned transaction table",
        },
        {
            "check_name": "Missing payment method",
            "affected_records": int(tx_raw["payment_method"].isna().sum()),
            "severity": "Medium",
            "resolution": "Imputed as Unknown",
        },
        {
            "check_name": "Transactions without matching user",
            "affected_records": int((~tx_raw["user_id"].isin(users_raw["user_id"])).sum()),
            "severity": "High",
            "resolution": "Removed from cleaned transaction table",
        },
        {
            "check_name": "Invalid user age",
            "affected_records": int((~users_raw["age"].between(18, 100)).sum()),
            "severity": "Medium",
            "resolution": "Set to median valid age",
        },
        {
            "check_name": "Clean user records",
            "affected_records": len(users),
            "severity": "Info",
            "resolution": "Final cleaned count",
        },
        {
            "check_name": "Clean transaction records",
            "affected_records": len(tx),
            "severity": "Info",
            "resolution": "Final cleaned count",
        },
    ]
    return pd.DataFrame(report)


def clean_users(users: pd.DataFrame) -> pd.DataFrame:
    users = users.drop_duplicates("user_id").copy()
    users["region"] = normalize_text(users["region"]).fillna("Unknown")
    users["acquisition_channel"] = normalize_text(users["acquisition_channel"]).fillna("Unknown")
    users["kyc_status"] = normalize_text(users["kyc_status"])
    users.loc[~users["kyc_status"].isin(["Verified", "Pending", "Rejected"]), "kyc_status"] = "Unknown"

    valid_age = users["age"].between(18, 100)
    median_age = int(users.loc[valid_age, "age"].median())
    users.loc[~valid_age, "age"] = median_age
    users["age"] = users["age"].astype(int)
    users["signup_month"] = users["signup_date"].dt.to_period("M").astype(str)
    return users


def clean_transactions(transactions: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    tx = transactions.drop_duplicates("transaction_id").copy()
    tx["status"] = normalize_text(tx["status"])
    tx["transaction_type"] = normalize_text(tx["transaction_type"])
    tx["payment_method"] = normalize_text(tx["payment_method"]).fillna("Unknown")
    tx["device_type"] = normalize_text(tx["device_type"])

    tx = tx[tx["amount"] > 0].copy()
    tx = tx[tx["user_id"].isin(users["user_id"])].copy()
    tx.loc[~tx["status"].isin(["Success", "Failed", "Pending", "Refunded"]), "status"] = "Unknown"
    tx["transaction_month"] = tx["transaction_date"].dt.to_period("M").astype(str)
    tx["transaction_day"] = tx["transaction_date"].dt.date.astype(str)
    return tx


def create_monthly_kpis(tx: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        tx.groupby("transaction_month")
        .agg(
            total_transactions=("transaction_id", "count"),
            active_users=("user_id", "nunique"),
            total_amount=("amount", "sum"),
            successful_amount=("amount", lambda s: s[tx.loc[s.index, "status"].eq("Success")].sum()),
            failed_transactions=("status", lambda s: s.eq("Failed").sum()),
            refunded_transactions=("status", lambda s: s.eq("Refunded").sum()),
        )
        .reset_index()
        .sort_values("transaction_month")
    )
    monthly["failed_transaction_rate"] = monthly["failed_transactions"] / monthly["total_transactions"]
    monthly["refund_rate"] = monthly["refunded_transactions"] / monthly["total_transactions"]
    monthly["avg_tx_per_active_user"] = monthly["total_transactions"] / monthly["active_users"]
    monthly["active_user_mom_change"] = monthly["active_users"].pct_change()
    return monthly.round(4)


def create_retention_cohorts(users: pd.DataFrame, tx: pd.DataFrame) -> pd.DataFrame:
    first_tx = tx.groupby("user_id")["transaction_date"].min().rename("first_transaction_date")
    activity = tx[["user_id", "transaction_date"]].merge(first_tx, on="user_id", how="left")
    activity = activity.merge(users[["user_id", "acquisition_channel", "region"]], on="user_id", how="left")
    activity["cohort_month"] = activity["first_transaction_date"].dt.to_period("M")
    activity["activity_month"] = activity["transaction_date"].dt.to_period("M")
    activity["months_since_first_tx"] = (
        (activity["activity_month"].dt.year - activity["cohort_month"].dt.year) * 12
        + activity["activity_month"].dt.month
        - activity["cohort_month"].dt.month
    )

    cohort = (
        activity.groupby(["cohort_month", "months_since_first_tx"])
        .agg(active_users=("user_id", "nunique"))
        .reset_index()
    )
    cohort_sizes = cohort[cohort["months_since_first_tx"].eq(0)][["cohort_month", "active_users"]]
    cohort_sizes = cohort_sizes.rename(columns={"active_users": "cohort_users"})
    cohort = cohort.merge(cohort_sizes, on="cohort_month")
    cohort["retention_rate"] = cohort["active_users"] / cohort["cohort_users"]
    cohort["cohort_month"] = cohort["cohort_month"].astype(str)
    return cohort.round(4)


def create_user_segments(users: pd.DataFrame, tx: pd.DataFrame) -> pd.DataFrame:
    max_date = tx["transaction_date"].max()
    user_metrics = (
        tx.groupby("user_id")
        .agg(
            transaction_count=("transaction_id", "count"),
            successful_transactions=("status", lambda s: s.eq("Success").sum()),
            total_spend=("amount", "sum"),
            first_transaction_date=("transaction_date", "min"),
            last_transaction_date=("transaction_date", "max"),
            active_months=("transaction_month", "nunique"),
        )
        .reset_index()
    )
    user_metrics["days_since_last_transaction"] = (max_date - user_metrics["last_transaction_date"]).dt.days
    user_metrics["avg_transaction_amount"] = user_metrics["total_spend"] / user_metrics["transaction_count"]
    user_metrics["engagement_segment"] = np.select(
        [
            (user_metrics["transaction_count"] >= 10) & (user_metrics["days_since_last_transaction"] <= 45),
            (user_metrics["transaction_count"] >= 5) & (user_metrics["days_since_last_transaction"] <= 90),
            user_metrics["days_since_last_transaction"] > 180,
        ],
        ["Power User", "Engaged", "At Risk"],
        default="Occasional",
    )
    return users.merge(user_metrics, on="user_id", how="left").fillna(
        {
            "transaction_count": 0,
            "successful_transactions": 0,
            "total_spend": 0,
            "active_months": 0,
            "days_since_last_transaction": 999,
            "avg_transaction_amount": 0,
            "engagement_segment": "No Activity",
        }
    )


def export_sqlite(
    users: pd.DataFrame,
    tx: pd.DataFrame,
    monthly: pd.DataFrame,
    cohorts: pd.DataFrame,
    segments: pd.DataFrame,
    quality_report: pd.DataFrame,
) -> None:
    db_path = OUTPUT_DIR / "fintech_retention.db"
    with sqlite3.connect(db_path) as conn:
        users.to_sql("users", conn, if_exists="replace", index=False)
        tx.to_sql("transactions", conn, if_exists="replace", index=False)
        monthly.to_sql("monthly_kpis", conn, if_exists="replace", index=False)
        cohorts.to_sql("retention_cohorts", conn, if_exists="replace", index=False)
        segments.to_sql("user_segments", conn, if_exists="replace", index=False)
        quality_report.to_sql("data_quality_report", conn, if_exists="replace", index=False)


def main() -> None:
    users_raw, tx_raw = load_raw()
    users = clean_users(users_raw)
    tx = clean_transactions(tx_raw, users)
    quality_report = build_quality_report(users_raw, tx_raw, users, tx)
    monthly_kpis = create_monthly_kpis(tx)
    retention_cohorts = create_retention_cohorts(users, tx)
    user_segments = create_user_segments(users, tx)

    users.to_csv(PROCESSED_DIR / "users_clean.csv", index=False)
    tx.to_csv(PROCESSED_DIR / "transactions_clean.csv", index=False)
    quality_report.to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)
    monthly_kpis.to_csv(OUTPUT_DIR / "monthly_kpis.csv", index=False)
    retention_cohorts.to_csv(OUTPUT_DIR / "retention_cohorts.csv", index=False)
    user_segments.to_csv(OUTPUT_DIR / "user_segments.csv", index=False)
    export_sqlite(users, tx, monthly_kpis, retention_cohorts, user_segments, quality_report)

    print("Analysis complete")
    print(f"Clean users: {len(users):,}")
    print(f"Clean transactions: {len(tx):,}")
    print(f"SQLite database: {OUTPUT_DIR / 'fintech_retention.db'}")


if __name__ == "__main__":
    main()
