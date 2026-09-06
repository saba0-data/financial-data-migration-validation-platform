import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


# -----------------------------
# PROJECT PATH CONFIGURATION
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------
# LOAD DATA
# -----------------------------

def load_data():

    customers = pd.read_csv(
        RAW_DATA_DIR / "customers.csv"
    )

    accounts = pd.read_csv(
        RAW_DATA_DIR / "accounts.csv"
    )

    transactions = pd.read_csv(
        RAW_DATA_DIR / "transactions.csv"
    )

    return customers, accounts, transactions


# -----------------------------
# CUSTOMER DATA ISSUES
# -----------------------------

def inject_customer_issues(customers):

    customers = customers.copy()

    # Missing customer ID
    customers.loc[0, "customer_id"] = None

    # Missing email
    customers.loc[1, "email"] = None

    # Invalid email
    customers.loc[2, "email"] = "invalid-email"

    # Duplicate customer ID
    customers.loc[3, "customer_id"] = customers.loc[4, "customer_id"]

    # Future created date
    future_date = datetime.today() + timedelta(days=30)

    customers.loc[5, "created_date"] = (
        future_date.strftime("%Y-%m-%d")
    )

    return customers


# -----------------------------
# ACCOUNT DATA ISSUES
# -----------------------------

def inject_account_issues(accounts):

    accounts = accounts.copy()

    # Missing customer ID
    accounts.loc[0, "customer_id"] = None

    # Negative balance
    accounts.loc[1, "balance"] = -5000

    # Invalid currency
    accounts.loc[2, "currency"] = "XYZ"

    # Invalid account type
    accounts.loc[3, "account_type"] = "PremiumGold"

    # Duplicate account ID
    accounts.loc[4, "account_id"] = accounts.loc[5, "account_id"]

    # Future account opening date
    future_date = datetime.today() + timedelta(days=60)

    accounts.loc[6, "account_open_date"] = (
        future_date.strftime("%Y-%m-%d")
    )

    return accounts


# -----------------------------
# TRANSACTION DATA ISSUES
# -----------------------------

def inject_transaction_issues(transactions):

    transactions = transactions.copy()

    # Missing account ID
    transactions.loc[0, "account_id"] = None

    # Negative amount
    transactions.loc[1, "amount"] = -1000

    # Zero amount
    transactions.loc[2, "amount"] = 0

    # Invalid currency
    transactions.loc[3, "currency"] = "ABC"

    # Invalid transaction type
    transactions.loc[4, "transaction_type"] = "Transfer"

    # Duplicate transaction ID
    transactions.loc[5, "transaction_id"] = (
        transactions.loc[6, "transaction_id"]
    )

    # Future transaction date
    future_date = datetime.today() + timedelta(days=10)

    transactions.loc[7, "transaction_date"] = (
        future_date.strftime("%Y-%m-%d")
    )

    # Invalid status
    transactions.loc[8, "status"] = "Unknown"

    return transactions


# -----------------------------
# SAVE CORRUPTED DATA
# -----------------------------

def save_data(customers, accounts, transactions):

    customers.to_csv(
        PROCESSED_DATA_DIR / "customers_with_issues.csv",
        index=False
    )

    accounts.to_csv(
        PROCESSED_DATA_DIR / "accounts_with_issues.csv",
        index=False
    )

    transactions.to_csv(
        PROCESSED_DATA_DIR / "transactions_with_issues.csv",
        index=False
    )

    print("\nData quality issues injected successfully!")

    print("\nIssues introduced:")

    print("Customers: 5 issues")
    print("Accounts: 6 issues")
    print("Transactions: 8 issues")


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    customers, accounts, transactions = load_data()

    customers = inject_customer_issues(
        customers
    )

    accounts = inject_account_issues(
        accounts
    )

    transactions = inject_transaction_issues(
        transactions
    )

    save_data(
        customers,
        accounts,
        transactions
    )