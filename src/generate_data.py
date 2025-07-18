from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *
from faker import Faker
import random
from datetime import datetime

# Initialize Faker
fake = Faker()

# Connect to your SQLite database
engine = create_engine("sqlite:////home/docutee/Code/Banking/database/banking.db")
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if not already created
Base.metadata.create_all(engine)

NUM_CUSTOMERS = 10

# Generate customers
for _ in range(NUM_CUSTOMERS):
    customer = Customer(
        customer_id=fake.uuid4(),
        full_name=fake.name(),
        date_of_birth=fake.date_of_birth().isoformat(),
        email=fake.email(),
        customer_pwd=fake.password(),
        phone_number=fake.phone_number(),
        created_at=fake.date_time_this_decade().isoformat()
    )
    
    customer_device = Device(
        device_id=fake.uuid4(),
        device_type=random.choice(["mobile", "tablet"]),
        os=random.choice(["Android", "iOS"]),
        is_verified=random.choice([True, False]),
        first_seen=fake.date_time_this_decade().isoformat(),
        last_seen=fake.date_time_this_decade().isoformat(),
        app_version = f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
    )

    # Generate a random identity type and number
    identity_type = random.choice(["passport", "national_id"])

    if identity_type == "national_id":
        # CCCD: 12-digit numeric string
        identity_number = "0" + "".join([str(random.randint(0, 9)) for _ in range(11)])
    else:
        # VN Passport: 1 uppercase letter + 7 digits
        prefix = random.choice("BCP")  # You can extend this list
        suffix = "".join([str(random.randint(0, 9)) for _ in range(7)])
        identity_number = prefix + suffix

    customer.identity = CustomerIdentity(
        identity_type=identity_type,
        identity_number=identity_number
    )

    # Accounts generation
    for _ in range(random.randint(1, 3)):  # Each customer can have 1 to 3 accounts
        account = Account(
            account_id=fake.uuid4(),
            customer_id=customer.customer_id,
            account_number="".join([str(random.randint(0, 9)) for _ in range(random.randint(9, 15))]),
            account_type=random.choice(["savings", "checking"]),
            balance=int(fake.pydecimal(left_digits=7, right_digits=0, positive=True)),
            acc_status=random.choice(["active", "inactive"]),
            date_opened=fake.date_time_this_decade().isoformat(),
            date_closed=None if random.choice([True, False]) else fake.date_time_this_decade().isoformat()
        )
        customer.accounts.append(account)

    session.add(customer)
    session.commit()
    print(f"Added customer: {customer.full_name} with ID: {customer.customer_id}")

# Case: Buy new device
customers_new_device = session.query(Customer).all()
customers_new_device = random.sample(customers_new_device, k = random.randint(0, min(10, len(customers_new_device))))

# Generate devices for customers
for customer in customers_new_device:
    device = Device(
        device_id=fake.uuid4(),
        device_type=random.choice(["mobile", "tablet"]),
        os=random.choice(["Android", "iOS"]),
        is_verified=False,
        first_seen=fake.date_time_this_decade().isoformat(),
        last_seen=fake.date_time_this_decade().isoformat(),
        app_version=f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
    )
    customer.devices.append(device)
    session.commit()
    print(f"Added new device for customer: {customer.full_name} with Device ID: {device.device_id}")

# Insert authentication methods
auth_methods = {
    "password": False,
    "otp": True,
    "biometric": True,
    "pin": False
}
for method, is_strong in auth_methods.items():
    auth_method = AuthenticationMethod(
        auth_method=method,
        is_strong=is_strong
    )
    session.add(auth_method)

# Verify devices
unverified_devices = session.query(Device).filter_by(is_verified=False).all()
for unverified_device in unverified_devices:
    print(f"Verifying device: {unverified_device.device_id} for customer: {unverified_device.customers[0].full_name}")
    unverified_device.is_verified = True
    authentication_log = AuthenticationLog(
        auth_log_id=fake.uuid4(),
        customer_id=unverified_device.customers[0].customer_id,
        device_id=unverified_device.device_id,
        auth_method=random.choice(session.query(AuthenticationMethod).all()).auth_method,
        auth_time=datetime.now().isoformat()
        status="verified",
        used_for="device_verification"

    )
    session.add(authentication_log)
    session.commit()
    print(f"Device {unverified_device.device_id} verified successfully.")

# Generate transactions for accounts
accounts = session.query(Account).all()
accounts = random.sample(accounts, k = random.randint(0, min(1000, len(accounts))))

for account in accounts:
    for _ in range(random.randint(1, 5)):  # Each account can have 1 to 5 transactions
        transaction_type = random.choice(["income", "expense"])
        transaction_amount = int(fake.pydecimal(left_digits=7, right_digits=0, positive=True))
        transaction_status = "failed"
        transaction = None
        if transaction_type == "income":
            account.balance += transaction_amount
            transaction = Transaction(
                transaction_id=fake.uuid4(),
                account_id=account.account_id,
                device_id=random.choice(account.customer.devices).device_id,
                amount=transaction_amount,
                transaction_type=transaction_type,
                transaction_time=datetime.now().isoformat(),
                description=fake.sentence() + f" destination: {random.choice(['ATM', 'Online Transfer', 'POS'])}, bank: {random.choice(['Bank A', 'Bank B', 'Bank C'])}, account: {account.account_number}."
                status=transaction_status,
                account=account,
                device=random.choice(account.customer.devices),
                auth_logs=[],
            )
        else:
            if account.balance >= transaction_amount:
                account.balance -= transaction_amount
                transaction_status = "success"
            else:
                transaction_status = "failed"
            transaction = Transaction(
                transaction_id=fake.uuid4(),
                account_id=account.account_id,
                device_id=random.choice(account.customer.devices).device_id,
                amount=transaction_amount,
                transaction_type=transaction_type,
                transaction_time=datetime.now().isoformat(),
                status=transaction_status,
                account=account,
                device=random.choice(account.customer.devices),
                auth_logs=[],
                description=fake.sentence() + f" destination: {random.choice(['ATM', 'Online Transfer', 'POS'])}, bank: {random.choice(['Bank A', 'Bank B', 'Bank C'])}, account: {account.account_number}."
            )
        # account.transactions.append(transaction)
        session.add(transaction)
        session.commit()