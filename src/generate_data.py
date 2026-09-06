from faker import Faker
import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

fake = Faker("en_IN")

# -----------------------------
# PROJECT PATH CONFIGURATION
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# CONFIGURATION
# -----------------------------

NUM_CUSTOMERS = 100
NUM_ACCOUNTS = 150
NUM_TRANSACTIONS = 500

VALID_CURRENCIES = ["INR", "USD", "EUR"]
ACCOUNT_TYPES = ["Savings", "Current"]
TRANSACTION_TYPES = ["Credit", "Debit"]
TRANSACTION_STATUS = ["Completed", "Pending", "Failed"]


# -----------------------------
# GENERATE CUSTOMERS
# -----------------------------

def generate_customers():

    customers = []

    for i in range(1, NUM_CUSTOMERS + 1):

        customer_id = f"CUST{i:04d}"

        customers.append({
            "customer_id": customer_id,
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.msisdn()[-10:],
            "city": fake.city(),
            "created_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            )
        })

    return pd.DataFrame(customers)


# -----------------------------
# GENERATE ACCOUNTS
# -----------------------------

def generate_accounts(customers):

    accounts = []

    customer_ids = customers["customer_id"].tolist()

    for i in range(1, NUM_ACCOUNTS + 1):

        account_id = f"ACC{i:05d}"

        customer_id = random.choice(customer_ids)

        accounts.append({
            "account_id": account_id,
            "customer_id": customer_id,
            "account_type": random.choice(ACCOUNT_TYPES),
            "balance": round(random.uniform(1000, 500000), 2),
            "currency": random.choice(VALID_CURRENCIES),
            "account_open_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            )
        })

    return pd.DataFrame(accounts)


# -----------------------------
# GENERATE TRANSACTIONS
# -----------------------------

def generate_transactions(accounts):

    transactions = []

    account_ids = accounts["account_id"].tolist()

    for i in range(1, NUM_TRANSACTIONS + 1):

        transaction_id = f"TXN{i:06d}"

        transactions.append({
            "transaction_id": transaction_id,
            "account_id": random.choice(account_ids),
            "transaction_date": fake.date_between(
                start_date="-1y",
                end_date="today"
            ),
            "transaction_type": random.choice(
                TRANSACTION_TYPES
            ),
            "amount": round(
                random.uniform(100, 100000),
                2
            ),
            "currency": random.choice(
                VALID_CURRENCIES
            ),
            "status": random.choice(
                TRANSACTION_STATUS
            )
        })

    return pd.DataFrame(transactions)


# -----------------------------
# SAVE DATA
# -----------------------------

def save_data(customers, accounts, transactions):

    customers.to_csv(
        RAW_DATA_DIR / "customers.csv",
        index=False
    )

    accounts.to_csv(
        RAW_DATA_DIR / "accounts.csv",
        index=False
    )

    transactions.to_csv(
        RAW_DATA_DIR / "transactions.csv",
        index=False
    )

    print("\nFinancial data generated successfully!")

    print(f"Customers: {len(customers)}")
    print(f"Accounts: {len(accounts)}")
    print(f"Transactions: {len(transactions)}")


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    customers = generate_customers()

    accounts = generate_accounts(customers)

    transactions = generate_transactions(accounts)

    save_data(
        customers,
        accounts,
        transactions
    )