from sqlalchemy.orm import sessionmaker
from model import *
from faker import Faker
import random
from datetime import datetime
from .gen_national_id import generate_national_id
from .gen_transaction import create_auth_log


def generate_customer_data(session: sessionmaker, num_customers: int = 100, fake: Faker = Faker('vi_VN'), today = datetime.now()):
    # Generate customers
    for _ in range(num_customers):
        customer = Customer(
            customer_id=fake.uuid4(),
            full_name=fake.name(),
            date_of_birth=fake.date_of_birth().isoformat(),
            email=fake.email(),
            customer_pwd=fake.password(),
            phone_number=fake.phone_number(),
            created_at=today.isoformat()
        )
        session.add(customer)
        session.commit()
        
        print(f"Added customer: {customer.full_name} with ID: {customer.customer_id}")

        # Generate a random device for the customer        
        customer_device = Device(
            device_id=fake.uuid4(),
            device_type=random.choice(["mobile", "tablet"]),
            os=random.choice(["Android", "iOS"]),
            is_verified=True,
            first_seen=today.isoformat(),
            last_seen=today.isoformat(),
            app_version = f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
        )
        customer_device.customers.append(customer)
        session.add(customer_device)

        authentication_log = create_auth_log(customer, customer_device, "biometric", "success", "device_verification")
        session.add(authentication_log)
        session.commit()

        # Generate a random identity type and number
        identity_type = random.choice(["passport", "national_id"])

        if identity_type == "national_id":
            identity_number = generate_national_id()
        else:
            # VN Passport: 1 uppercase letter + 7 digits
            prefix = random.choice("BCP")
            suffix = "".join([str(random.randint(0, 9)) for _ in range(7)])
            identity_number = prefix + suffix

        customer.identity = CustomerIdentity(
            identity_type=identity_type,
            identity_number=identity_number
        )
        session.add(customer)
        session.commit()

        # Accounts generation
        for _ in range(random.randint(1, 3)):  # Each customer can have 1 to 3 accounts
            account = Account(
                account_id=fake.uuid4(),
                customer_id=customer.customer_id,
                account_number="".join([str(random.randint(0, 9)) for _ in range(random.randint(9, 15))]),
                account_type=random.choice(["savings", "checking"]),
                balance=int(fake.pydecimal(left_digits=8, right_digits=0, positive=True)),
                acc_status=random.choice(["active", "inactive"]),
                date_opened=fake.date_time_this_decade().isoformat(),
                date_closed=None if random.choice([True, False]) else fake.date_time_this_decade().isoformat()
            )
            customer.accounts.append(account)
            print(f"Added account: {account.account_number} for customer: {customer.full_name}")
            session.add(account)
            session.commit()

        