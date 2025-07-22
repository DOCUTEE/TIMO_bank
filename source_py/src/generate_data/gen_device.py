from sqlalchemy.orm import sessionmaker
from model import *
from faker import Faker
import random
from datetime import datetime

def generate_new_customer_device(session: sessionmaker, customers, fake: Faker = Faker('vi_VN'), today=datetime.now()):
    for customer in customers:
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
