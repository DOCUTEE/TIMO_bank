from faker import Faker

# Initialize Faker 
faker = Faker(['vi_VN', 'en_US'])  # Vietnamese and English locales
Faker.seed(0)  # For reproducibility