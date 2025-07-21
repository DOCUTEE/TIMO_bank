import random

def generate_national_id():
    # 3-digit province code (starts with 0, range: 001–099 for realism)
    province_code = f"0{random.randint(1, 99):02d}"

    # Gender + century code:
    # 0: Male 1900–1999, 1: Female 1900–1999
    # 2: Male 2000–2099, 3: Female 2000–2099
    gender_century_code = random.choice(["0", "1", "2", "3"])

    # 2-digit year of birth (00–99)
    year_of_birth = f"{random.randint(0, 99):02d}"

    # 6-digit personal identifier
    personal_code = f"{random.randint(0, 999999):06d}"

    # Final CCCD
    national_id = province_code + gender_century_code + year_of_birth + personal_code
    return national_id