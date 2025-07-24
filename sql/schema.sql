CREATE TABLE IF NOT EXISTS customer (
    customer_id VARCHAR PRIMARY KEY,
    full_name VARCHAR,
    date_of_birth VARCHAR,
    email VARCHAR,
    customer_pwd VARCHAR,
    phone_number VARCHAR,
    created_at VARCHAR
);

CREATE TABLE IF NOT EXISTS device (
    device_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    device_type VARCHAR,
    os VARCHAR,
    is_verified BOOLEAN,
    first_seen VARCHAR,
    last_seen VARCHAR,
    app_version VARCHAR,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS account (
    account_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    account_number VARCHAR,
    account_type VARCHAR,
    balance BIGINT,
    acc_status VARCHAR,
    date_opened VARCHAR,
    date_closed VARCHAR,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS transaction_log (
    transaction_id VARCHAR PRIMARY KEY,
    account_id VARCHAR,
    device_id VARCHAR,
    amount BIGINT,
    transaction_type VARCHAR,
    transaction_time VARCHAR,
    description VARCHAR,
    status VARCHAR,
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);

CREATE TABLE IF NOT EXISTS customer_identity (
    customer_id VARCHAR,
    identity_type VARCHAR,
    identity_number VARCHAR,
    PRIMARY KEY (customer_id, identity_type),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS authentication (
    auth_method VARCHAR PRIMARY KEY,
    is_strong BOOLEAN
);

CREATE TABLE IF NOT EXISTS authentication_log (
    auth_log_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    device_id VARCHAR,
    auth_method VARCHAR,
    auth_time VARCHAR,
    status VARCHAR,
    used_for VARCHAR,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (device_id) REFERENCES device(device_id),
    FOREIGN KEY (auth_method) REFERENCES authentication(auth_method)
);

CREATE TABLE IF NOT EXISTS customer_risk (
    risk_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    detected_time VARCHAR,
    details VARCHAR,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS device_risk (
    risk_id VARCHAR PRIMARY KEY,
    device_id VARCHAR,
    detected_time VARCHAR,
    details VARCHAR,
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);

CREATE TABLE IF NOT EXISTS transaction_risk (
    risk_id VARCHAR PRIMARY KEY,
    transaction_id VARCHAR,
    detected_time VARCHAR,
    details VARCHAR,
    FOREIGN KEY (transaction_id) REFERENCES transaction_log(transaction_id)
);

CREATE TABLE IF NOT EXISTS customer_device (
    customer_id VARCHAR,
    device_id VARCHAR,
    PRIMARY KEY (customer_id, device_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);

CREATE TABLE IF NOT EXISTS auth_transaction (
    transaction_id VARCHAR,
    auth_log_id VARCHAR,
    PRIMARY KEY (transaction_id, auth_log_id),
    FOREIGN KEY (transaction_id) REFERENCES transaction_log(transaction_id),
    FOREIGN KEY (auth_log_id) REFERENCES authentication_log(auth_log_id)
);
