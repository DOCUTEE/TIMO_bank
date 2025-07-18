from models import Device
from data_faker.data_faker import faker  # Importing the initialized Faker instance
from datetime import datetime
import uuid
import random

def generate_devices_for_customers(customers):
    if (customers is None) or (len(customers) == 0):
        print("No customers provided to generate devices.")
        return
    devices = []
    for customer in customers:
        for _ in range(random.randint(1, 3)):  # Generate 1 to 3 devices per customer
            device = Device(
                device_id=uuid.uuid4().hex,
                customer_id=customer.customer_id,
                device_type=faker.random_element(elements=('mobile', 'tablet')),
                os=faker.random_element(elements=('iOS', 'Android')),
                is_verified=random.randint(0, 1),
                first_seen=datetime.now().isoformat(),
                last_seen=datetime.now().isoformat(),
                app_version=f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                device_fingerprint=uuid.uuid4().hex
            )
            devices.append(device)
    return devices
