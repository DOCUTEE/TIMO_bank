from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer
from datetime import datetime
import uuid
from faker import Faker

# Initialize Faker
fake = Faker()

# 1. Connect to your SQLite database
engine = create_engine("sqlite:////home/docutee/Code/Banking/database/banking.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# 2. (Optional) Create tables if not already created
Base.metadata.create_all(engine)


