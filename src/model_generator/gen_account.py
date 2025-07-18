from data_faker.data_faker import faker  # Importing the initialized Faker instance
from datetime import datetime
import uuid
from models import Account
import random

def generate_accounts_for_customers(customers):
    if (customers is None) or (len(customers) == 0):
        print("No customers provided to generate accounts.")
        return
    accounts_map = {}
    for customer in customers:
        customer_accounts = []
        for _ in range(random.randint(1, 5)):
            account = Account(
                account_id=uuid.uuid4().hex,
                customer_id=customer.customer_id,
                account_number=faker.bban(),
                account_type=faker.random_element(elements=('savings', 'checking')),
                balance=int(faker.pydecimal(left_digits=5, right_digits=0, positive=True)),
                acc_status=faker.random_element(elements=('active', 'inactive')),
                date_opened=datetime.now().isoformat(),
                date_closed=None
            )
            customer_accounts.append(account)
        accounts_map[customer] = customer_accounts  # Use customer object as key
    return accounts_map
        
        
