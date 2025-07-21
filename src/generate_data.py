from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from model import *
from faker import Faker
import random
from datetime import datetime
import os
from generate_data import *

# Initialize Faker
fake = Faker(['vi_VN'])  # Vietnamese and English locales

# Connect to your SQLite database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'banking.db')
engine = create_engine(f"sqlite:///{os.path.abspath(db_path)}", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if not already created
Base.metadata.create_all(engine)

NUM_CUSTOMERS = 100

# Generate customers
generate_customer_data(session, num_customers=NUM_CUSTOMERS, fake=fake)

# Case: Buy new device
customers_new_device = session.query(Customer).all()
customers_new_device = random.sample(customers_new_device, k = random.randint(0, min(100, len(customers_new_device))))

# Generate devices for customers
generate_new_customer_device(session, customers=customers_new_device, fake=fake)

# Insert authentication methods if not exist
generate_auth_methods(session)

# Verify devices
unverified_devices = session.query(Device).filter_by(is_verified=False).all()
verify_unverified_devices(session, fake=fake, unverified_devices=unverified_devices)

# Generate transactions for accounts
accounts = session.query(Account).all()
accounts = random.sample(accounts, k = random.randint(0, min(1000, len(accounts))))

generate_transaction_data(session, accounts=accounts, fake=fake)
    