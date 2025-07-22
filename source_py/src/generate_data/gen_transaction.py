from sqlalchemy.orm import sessionmaker
from model import TransactionLog, AuthTransaction, AuthenticationLog
from datetime import datetime
import random
from faker import Faker
from sqlalchemy import func

fake = Faker('vi_VN')


def create_transaction(account, device, amount, txn_type, status, auth_logs=[]):
    return TransactionLog(
        transaction_id=fake.uuid4(),
        account_id=account.account_id,
        device_id=device.device_id,
        amount=amount,
        transaction_type=txn_type,
        transaction_time=datetime.now().isoformat(),
        description=fake.sentence() + f" destination: {random.choice(['ATM', 'Online Transfer', 'POS'])}, bank: {random.choice(['Bank A', 'Bank B', 'Bank C'])}, account: {account.account_number}.",
        status=status,
        account=account,
        device=device,
        auth_logs=auth_logs
    )


def create_auth_log(customer, device, method, status, purpose):
    return AuthenticationLog(
        auth_log_id=fake.uuid4(),
        customer_id=customer.customer_id,
        device_id=device.device_id,
        auth_method=method,
        auth_time=datetime.now().isoformat(),
        status=status,
        used_for=purpose
    )


def handle_income(session, account, amount, device):
    account.balance += amount
    txn = create_transaction(account, device, amount, "income", "success")
    session.add(txn)
    print_transaction(txn, account.balance)


def handle_expense(session, account, amount, device):
    if account.balance < amount:
        print(f"Insufficient balance for {amount} VND on account {account.account_number}")
        return

    account.balance -= amount
    
    today = datetime.now().date().isoformat()
    total_today = session.query(func.sum(TransactionLog.amount)).filter(
        TransactionLog.account_id == account.account_id,
        TransactionLog.transaction_type == 'expense',
        func.date(TransactionLog.transaction_time) == today,
        TransactionLog.transaction_time <= datetime.now().isoformat()
    ).scalar() or 0
    over_20M_auth = None
    txn = create_transaction(account, device, amount, "expense", "failed", [])
    if total_today > 20_000_000:
        print(f"Account {account.account_number} exceeds 20M VND today. Creating biometric auth.")
        status = "success"  # Assume biometric auth is always successful
        if not random.choice([True, False]):
            status = "failed"
        over_20M_auth_log = create_auth_log(account.customer, device, "biometric", status, "authentication_over_20M")
        over_20M_auth = AuthTransaction(transaction=txn, auth_log=over_20M_auth_log)
        session.add(over_20M_auth)
        session.commit()

    auth_patterns = [["success", "failed"], ["failed"], ["success", "success"]]
    auth_result = random.choice(auth_patterns)
    txn_status = "success" if auth_result == ["success", "success"] else "failed"
    txn.status = txn_status
    if over_20M_auth:
        txn.auth_logs.append(over_20M_auth)

    for idx, status in enumerate(auth_result):
        method = "biometric" if idx == 0 and amount > 10_000_000 else ("pin" if idx == 0 else "otp")
        auth_log = create_auth_log(account.customer, device, method, status, "transaction")
        auth_txn = AuthTransaction(transaction=None, auth_log=auth_log)
        txn.auth_logs.append(auth_txn)
    
    session.add(txn)
    session.commit()
    print_transaction(txn, account.balance)


def print_transaction(txn, balance):
    print(
        f"""
        Transaction ID: {txn.transaction_id}
        Account ID: {txn.account_id}
        Device ID: {txn.device_id}
        Amount: {txn.amount}
        Type: {txn.transaction_type}
        Time: {txn.transaction_time}
        Status: {txn.status}
        Balance: {balance}
        """
    )


def generate_transaction_data(session: sessionmaker, accounts, fake=fake):
    for account in accounts:
        verified_devices = [d for d in account.customer.devices if d.is_verified]
        if not verified_devices:
            continue

        for _ in range(random.randint(1, 5)):
            txn_type = random.choice(["income", "expense"])
            amount = random.randint(1000, 50000000)
            device = random.choice(verified_devices)

            if txn_type == "income":
                handle_income(session, account, amount, device)
            else:
                handle_expense(session, account, amount, device)

            session.commit()
