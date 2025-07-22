from sqlalchemy import create_engine, inspect, text
from check_data import *
import sys

if __name__ == "__main__":
    try:
        # Connect to your PostgreSQL database 
        engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow", echo=True)

        # Example usage
        check_nulls(engine)
        check_uniqueness(engine)
        check_identity_number_uniqueness(engine)
        check_national_id_format(engine)
        check_foreign_keys_account_customer(engine)
        check_foreign_keys_transaction_log_account(engine)
        check_foreign_keys_transaction_log_device(engine)
        check_foreign_keys_customer_identity(engine)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)