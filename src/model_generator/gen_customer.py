from models import Customer 
from data_faker.data_faker import faker  # Importing the initialized Faker instance
from datetime import datetime
import uuid

NUM_CUSTOMERS = 10

# Generate customer data
def generate_customers(number_of_customers=NUM_CUSTOMERS):
    
    customers = []

    for _ in range(number_of_customers):
        id_type = faker.random_element(elements=('passport', 'national_id'))
        id_number = faker.passport_number() if id_type == 'passport' else faker.ssn()
        customer = Customer(
            customer_id=uuid.uuid4().hex,
            full_name=faker.name(),
            date_of_birth=str(faker.date_of_birth(minimum_age=18, maximum_age=80)),
            email=faker.email(),
            phone_number=faker.phone_number(),
            identity_type=id_type,
            identity_number=id_number,
            created_at=datetime.now().isoformat()
        )
        customers.append(customer)
    
    return customers
