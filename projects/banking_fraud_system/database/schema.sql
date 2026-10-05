-- Banking Fraud Detection System Database Schema
CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    holder_name TEXT NOT NULL,
    balance REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    timestamp TIMESTAMP NOT NULL,
    mcc TEXT DEFAULT '5411: GROCERIES',
    channel TEXT DEFAULT 'ONLINE',
    device_id TEXT,
    ip_address TEXT,
    card_present INTEGER DEFAULT 0,
    cvv_verified INTEGER DEFAULT 1,
    location_lat REAL,
    location_lon REAL,
    status TEXT DEFAULT 'COMPLETED',
    FOREIGN KEY (account_id) REFERENCES accounts (account_id)
);

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    risk_score REAL NOT NULL,
    triggered_rules TEXT NOT NULL,
    decision TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions (transaction_id),
    FOREIGN KEY (account_id) REFERENCES accounts (account_id)
);

CREATE INDEX IF NOT EXISTS idx_transactions_acc_time ON transactions(account_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_acc ON fraud_alerts(account_id);
