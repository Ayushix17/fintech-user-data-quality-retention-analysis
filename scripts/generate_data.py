from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(42)


def random_dates(start: str, end: str, size: int) -> pd.Series:
    start_ts = pd.Timestamp(start).value // 10**9
    end_ts = pd.Timestamp(end).value // 10**9
    return pd.to_datetime(RNG.integers(start_ts, end_ts, size), unit="s")


def generate_users(n_users: int = 12000) -> pd.DataFrame:
    signup_dates = random_dates("2023-01-01", "2024-12-31", n_users)
    users = pd.DataFrame(
        {
            "user_id": [f"U{idx:06d}" for idx in range(1, n_users + 1)],
            "signup_date": signup_dates,
            "age": RNG.integers(18, 71, n_users),
            "region": RNG.choice(
                ["North", "South", "East", "West", "Central"],
                n_users,
                p=[0.24, 0.22, 0.19, 0.21, 0.14],
            ),
            "acquisition_channel": RNG.choice(
                ["Organic", "Paid Search", "Referral", "Affiliate", "Social"],
                n_users,
                p=[0.34, 0.24, 0.2, 0.1, 0.12],
            ),
            "kyc_status": RNG.choice(
                ["Verified", "Pending", "Rejected"],
                n_users,
                p=[0.82, 0.13, 0.05],
            ),
        }
    )

    dirty_idx = RNG.choice(users.index, int(n_users * 0.025), replace=False)
    users.loc[dirty_idx[:100], "region"] = None
    users.loc[dirty_idx[100:180], "age"] = RNG.choice([-5, 0, 110, 140], 80)
    users.loc[dirty_idx[180:240], "kyc_status"] = "unknown"
    users.loc[dirty_idx[240:], "acquisition_channel"] = "paid search "
    return users


def generate_transactions(users: pd.DataFrame, n_transactions: int = 52000) -> pd.DataFrame:
    user_ids = RNG.choice(users["user_id"], n_transactions, replace=True)
    tx_dates = random_dates("2023-01-01", "2025-03-31", n_transactions)
    categories = ["Wallet Load", "P2P Transfer", "Bill Payment", "Card Spend", "Investment"]

    transactions = pd.DataFrame(
        {
            "transaction_id": [f"T{idx:08d}" for idx in range(1, n_transactions + 1)],
            "user_id": user_ids,
            "transaction_date": tx_dates,
            "amount": RNG.lognormal(mean=4.6, sigma=0.85, size=n_transactions).round(2),
            "transaction_type": RNG.choice(categories, n_transactions, p=[0.25, 0.28, 0.2, 0.19, 0.08]),
            "status": RNG.choice(
                ["Success", "Failed", "Pending", "Refunded"],
                n_transactions,
                p=[0.84, 0.08, 0.05, 0.03],
            ),
            "payment_method": RNG.choice(
                ["UPI", "Debit Card", "Credit Card", "Net Banking", "Wallet"],
                n_transactions,
                p=[0.4, 0.18, 0.16, 0.14, 0.12],
            ),
            "device_type": RNG.choice(["Android", "iOS", "Web"], n_transactions, p=[0.58, 0.28, 0.14]),
        }
    )

    dirty_idx = RNG.choice(transactions.index, int(n_transactions * 0.035), replace=False)
    transactions.loc[dirty_idx[:300], "amount"] = RNG.choice([-999, -10, 0], 300)
    transactions.loc[dirty_idx[300:520], "status"] = RNG.choice(["success", "FAILED", "unknown"], 220)
    transactions.loc[dirty_idx[520:700], "payment_method"] = None
    transactions.loc[dirty_idx[700:850], "transaction_type"] = "bill payment "

    duplicate_rows = transactions.sample(260, random_state=42)
    transactions = pd.concat([transactions, duplicate_rows], ignore_index=True)

    orphan_rows = transactions.sample(80, random_state=99).copy()
    orphan_rows["transaction_id"] = [f"T9999{idx:04d}" for idx in range(len(orphan_rows))]
    orphan_rows["user_id"] = [f"MISSING{idx:04d}" for idx in range(len(orphan_rows))]
    transactions = pd.concat([transactions, orphan_rows], ignore_index=True)

    return transactions.sample(frac=1, random_state=42).reset_index(drop=True)


def main() -> None:
    users = generate_users()
    transactions = generate_transactions(users)

    users.to_csv(RAW_DIR / "users_raw.csv", index=False)
    transactions.to_csv(RAW_DIR / "transactions_raw.csv", index=False)

    print(f"Generated {len(users):,} users -> {RAW_DIR / 'users_raw.csv'}")
    print(f"Generated {len(transactions):,} transactions -> {RAW_DIR / 'transactions_raw.csv'}")


if __name__ == "__main__":
    main()
