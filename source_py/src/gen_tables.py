from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from model import *
from faker import Faker
import random
from datetime import datetime
import os
from generate_data import *

if __name__ == "__main__":

    # Initialize Faker
    fake = Faker(['vi_VN'])  # Vietnamese locale

    # Connect to your PostgreSQL database
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow", echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables if not already created
    Base.metadata.create_all(engine)