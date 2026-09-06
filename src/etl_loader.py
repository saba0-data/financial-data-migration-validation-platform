import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine


# -----------------------------
# PROJECT PATHS
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CLEANED_DATA_DIR = BASE_DIR / "data" / "cleaned"

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = (
    DATABASE_DIR /
    "financial_data.db"
)


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# -----------------------------
# LOAD CLEANED DATA
# -----------------------------

def load_cleaned_data():

    customers = pd.read_csv(
        CLEANED_DATA_DIR /
        "customers_cleaned.csv"
    )

    accounts = pd.read_csv(
        CLEANED_DATA_DIR /
        "accounts_cleaned.csv"
    )

    transactions = pd.read_csv(
        CLEANED_DATA_DIR /
        "transactions_cleaned.csv"
    )

    return customers, accounts, transactions


# -----------------------------
# LOAD DATA TO TARGET
# -----------------------------

def load_to_database(
    customers,
    accounts,
    transactions
):

    customers.to_sql(
        "customers",
        engine,
        if_exists="replace",
        index=False
    )

    accounts.to_sql(
        "accounts",
        engine,
        if_exists="replace",
        index=False
    )

    transactions.to_sql(
        "transactions",
        engine,
        if_exists="replace",
        index=False
    )

    print("\nData loaded successfully!")

    print(
        f"Customers loaded: "
        f"{len(customers)}"
    )

    print(
        f"Accounts loaded: "
        f"{len(accounts)}"
    )

    print(
        f"Transactions loaded: "
        f"{len(transactions)}"
    )


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    customers, accounts, transactions = (
        load_cleaned_data()
    )

    load_to_database(
        customers,
        accounts,
        transactions
    )