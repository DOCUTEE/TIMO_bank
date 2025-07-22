from sqlalchemy.orm import sessionmaker
from model import Device, AuthenticationLog, AuthenticationMethod
import random
from faker import Faker
from datetime import datetime

def verify_unverified_devices(session : sessionmaker, fake : Faker = Faker('vi_VN'), unverified_devices=None):
    """Verify unverified devices and log the verification."""
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