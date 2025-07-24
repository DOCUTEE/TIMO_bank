# Data Generation Modules

This folder contains Python modules for generating synthetic banking data. Below is a high-level description of the algorithm in each module:

---

## gen_customer.py

**Algorithm:**
- For each customer to generate:
  - Create a customer with random personal info.
  - Assign a verified device and log a biometric authentication.
  - Generate and link a random identity (national ID or passport).
  - Create 1–3 accounts for the customer with random details.

---

## gen_device.py

**Algorithm:**
- For a given list of customers:
  - For each customer, create a new device with random attributes.
  - Link the device to the customer and mark as verified or unverified as needed.

---

## gen_auth_method.py

**Algorithm:**
- Check if each authentication method (password, OTP, biometric, PIN) exists.
- If not, insert it into the database with its "strong" status.

---

## gen_device_verify_action.py

**Algorithm:**
- Find all unverified devices.
- For a random subset, mark them as verified and log the verification action.

---

## gen_transaction.py

**Algorithm:**
- For a given list of accounts:
  - Generate random transactions (income/expense) for each account.
  - For each transaction, create and link authentication logs.
  - Assign transactions to accounts and devices.
