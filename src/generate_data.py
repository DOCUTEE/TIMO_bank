from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *
from faker import Faker
import random
from datetime import datetime
import os

# Initialize Faker
fake = Faker()

# Connect to your SQLite database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'banking.db')
engine = create_engine(f"sqlite:///{os.path.abspath(db_path)}")
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if not already created
Base.metadata.create_all(engine)

NUM_CUSTOMERS = 3

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

customers_new_device = []
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

# Insert authentication methods if not exist
auth_methods = {
    "password": False,
    "otp": True,
    "biometric": True,
    "pin": False
}
for method, is_strong in auth_methods.items():
    exists = session.query(AuthenticationMethod).filter_by(auth_method=method).first()
    if not exists:
        auth_method = AuthenticationMethod(
            auth_method=method,
            is_strong=is_strong
        )
        session.add(auth_method)
session.commit()

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
        auth_time=datetime.now().isoformat(),
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
        # Choose a verified device if available, else any device
        verified_devices = [d for d in account.customer.devices if d.is_verified]
        if verified_devices:
            device_for_transaction = random.choice(verified_devices)
        else:
            continue
        if transaction_type == "income":
            account.balance += transaction_amount
            transaction = TransactionLog(
                transaction_id=fake.uuid4(),
                account_id=account.account_id,
                device_id=random.choice(account.customer.devices).device_id,
                amount=transaction_amount,
                transaction_type=transaction_type,
                transaction_time=datetime.now().isoformat(),
                description=fake.sentence() + f" destination: {random.choice(['ATM', 'Online Transfer', 'POS'])}, bank: {random.choice(['Bank A', 'Bank B', 'Bank C'])}, account: {account.account_number}.",
                status= "success",
                account=account,
                device=device_for_transaction,
                auth_logs=[]
            )
            session.add(transaction)
            
            print(
                f'''
                Transaction ID: {transaction.transaction_id}
                Account ID: {account.account_id}    
                Device ID: {device_for_transaction.device_id}
                Amount: {transaction_amount}
                Transaction Type: {transaction_type}
                Transaction Time: {transaction.transaction_time}
                Description: {transaction.description}
                Status: {transaction.status}
                Account Balance after transaction: {account.balance}
                '''
            )
            # session.commit()
        else:
            if account.balance >= transaction_amount:
                account.balance -= transaction_amount
                # Have 2 cases: success and failed in auth logs
                list_of_auth_results = [
                    ["success", "failed"],
                    ["failed"],
                    ["success", "success"]
                ]
                for auth_result in list_of_auth_results:
                    if (["success", "success"] in auth_result):
                        transaction_status = "success"
                    else:
                        transaction_status = "failed"
                    transaction = TransactionLog(
                        transaction_id=fake.uuid4(),
                        account_id=account.account_id,
                        device_id=random.choice(account.customer.devices).device_id,
                        amount=transaction_amount,
                        transaction_type=transaction_type,
                        transaction_time=datetime.now().isoformat(),
                        description=fake.sentence() + f" destination: {random.choice(['ATM', 'Online Transfer', 'POS'])}, bank: {random.choice(['Bank A', 'Bank B', 'Bank C'])}, account: {account.account_number}.",
                        status=transaction_status,
                        account=account,
                        device=device_for_transaction,
                        auth_logs=[]
                    )
                    session.add(transaction)
                    
                    # Create an authentication log for the transaction
                    for index, auth_status in enumerate(auth_result):
                        if (index == 0):
                            if transaction_amount > 10000000:
                                auth_method= "biometric"
                            else:
                                auth_method = "pin"
                        else:
                            auth_method = 'otp'
                        
                        transaction.auth_logs.append(
                            AuthTransaction(
                                transaction = transaction,
                                auth_log = AuthenticationLog(
                                    auth_log_id=fake.uuid4(),
                                    customer_id=account.customer.customer_id,
                                    device_id=random.choice(account.customer.devices).device_id,
                                    auth_method=auth_method,
                                    auth_time=datetime.now().isoformat(),
                                    status=auth_status,
                                    used_for="transaction"
                                )
                            )
                        )
                    session.add(transaction)
                    print(
                        f'''
                        Transaction ID: {transaction.transaction_id}
                        Account ID: {account.account_id}    
                        Device ID: {device_for_transaction.device_id}
                        Amount: {transaction_amount}
                        Transaction Type: {transaction_type}
                        Transaction Time: {transaction.transaction_time}
                        Description: {transaction.description}
                        Status: {transaction.status}
                        Account Balance after transaction: {account.balance}
                        '''
                    )
            else:
                print(f"Insufficient balance for transaction of {transaction_amount} on account {account.account_number}. Skipping transaction.")
                continue
        
        session.commit()
    