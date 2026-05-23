CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    signup_date TEXT NOT NULL,
    age INTEGER NOT NULL,
    region TEXT NOT NULL,
    acquisition_channel TEXT NOT NULL,
    kyc_status TEXT NOT NULL,
    signup_month TEXT NOT NULL
);

CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,
    status TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    device_type TEXT NOT NULL,
    transaction_month TEXT NOT NULL,
    transaction_day TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_month ON transactions(transaction_month);
CREATE INDEX idx_transactions_status ON transactions(status);
