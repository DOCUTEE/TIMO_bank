CREATE TABLE IF NOT EXISTS customer (
    customer_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    created_at TEXT,
    phone_number TEXT,
    email TEXT
);

CREATE TABLE customer_identity (
    identity_type TEXT,
    identity_number TEXT,
    customer_id TEXT,
    PRIMARY KEY (identity_type, identity_number),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);


CREATE TABLE IF NOT EXISTS account (
    account_id TEXT PRIMARY KEY,
    customer_id TEXT,
    account_number TEXT,
    account_type TEXT,
    balance REAL,
    acc_status TEXT,
    date_opened TEXT,
    date_closed TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS device (
    device_id TEXT PRIMARY KEY,
    customer_id TEXT,
    device_type TEXT,
    os TEXT,
    is_verified INTEGER,
    first_seen TEXT,
    last_seen TEXT,
    app_version TEXT,
    device_fingerprint TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS authentication_method (
    auth_method TEXT PRIMARY KEY,
    is_strong INTEGER
);

CREATE TABLE IF NOT EXISTS authentication_log (
    auth_log_id TEXT PRIMARY KEY,
    customer_id TEXT,
    device_id TEXT,
    auth_method TEXT,
    auth_time TEXT,
    status TEXT,
    used_for TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (device_id) REFERENCES device(device_id),
    FOREIGN KEY (transaction_id) REFERENCES transaction_record(transaction_id),
    FOREIGN KEY (auth_method) REFERENCES authentication(auth_method)
);

CREATE TABLE IF NOT EXISTS transaction_record (
    transaction_id TEXT PRIMARY KEY,
    account_id TEXT,
    device_id TEXT,
    auth_id TEXT,
    amount REAL,
    transaction_type TEXT,
    transaction_time TEXT,
    used_strong_auth INTEGER,
    current_balance REAL,
    description TEXT,
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (device_id) REFERENCES device(device_id),
    FOREIGN KEY (auth_id) REFERENCES authentication_log(auth_log_id)
);

CREATE TABLE IF NOT EXISTS customer_risk (
    risk_id TEXT PRIMARY KEY,
    customer_id TEXT,
    detected_time TEXT,
    details TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS transaction_risk (
    risk_id TEXT PRIMARY KEY,
    transaction_id TEXT,
    detected_time TEXT,
    details TEXT,
    FOREIGN KEY (transaction_id) REFERENCES transaction_record(transaction_id)
);

CREATE TABLE IF NOT EXISTS device_risk (
    risk_id TEXT PRIMARY KEY,
    device_id TEXT,
    detected_time TEXT,
    details TEXT,
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);
