from sqlalchemy import create_engine, inspect, text
from models import Base  # your schema above saved in models.py
from check_data import *

# Replace with your actual DB URI
engine = create_engine("sqlite:////workspaces/TIMO_bank/database/banking.db")

# Example usage
check_nulls(engine)
check_uniqueness(engine)
check_identity_number_uniqueness(engine)
check_national_id_format(engine)
