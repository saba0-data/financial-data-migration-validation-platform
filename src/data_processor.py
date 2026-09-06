import pandas as pd
from pathlib import Path


# -----------------------------
# PROJECT PATHS
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
CLEANED_DATA_DIR = BASE_DIR / "data" / "cleaned"
INVALID_DATA_DIR = BASE_DIR / "data" / "invalid"

REPORTS_DIR = BASE_DIR / "reports"


CLEANED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INVALID_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------
# LOAD DATA
# -----------------------------

def load_data():

    customers = pd.read_csv(
        PROCESSED_DATA_DIR /
        "customers_with_issues.csv"
    )

    accounts = pd.read_csv(
        PROCESSED_DATA_DIR /
        "accounts_with_issues.csv"
    )

    transactions = pd.read_csv(
        PROCESSED_DATA_DIR /
        "transactions_with_issues.csv"
    )

    issues = pd.read_csv(
        REPORTS_DIR /
        "data_quality_report.csv"
    )

    return customers, accounts, transactions, issues


# -----------------------------
# SPLIT DIRECTLY INVALID RECORDS
# -----------------------------

def get_invalid_rows(
    data,
    table_name,
    issues
):

    table_issues = issues[
        issues["table"] == table_name
    ]

    invalid_rows = set(
        table_issues["row"]
    )

    invalid_data = data.loc[
        data.index.isin(invalid_rows)
    ].copy()

    valid_data = data.loc[
        ~data.index.isin(invalid_rows)
    ].copy()

    return valid_data, invalid_data


# -----------------------------
# APPLY DATA DEPENDENCIES
# -----------------------------

def apply_dependencies(
    valid_customers,
    valid_accounts,
    valid_transactions,
    invalid_accounts,
    invalid_transactions
):

    # -------------------------
    # ACCOUNTS → CUSTOMERS
    # -------------------------

    valid_customer_ids = set(
        valid_customers["customer_id"]
        .dropna()
        .astype(str)
    )

    invalid_account_dependency = (
        ~valid_accounts["customer_id"]
        .astype(str)
        .isin(valid_customer_ids)
    )

    dependency_invalid_accounts = (
        valid_accounts[
            invalid_account_dependency
        ].copy()
    )

    valid_accounts = (
        valid_accounts[
            ~invalid_account_dependency
        ].copy()
    )


    # Add dependency-invalid accounts

    invalid_accounts = pd.concat(
        [
            invalid_accounts,
            dependency_invalid_accounts
        ],
        ignore_index=True
    )


    # -------------------------
    # TRANSACTIONS → ACCOUNTS
    # -------------------------

    valid_account_ids = set(
        valid_accounts["account_id"]
        .dropna()
        .astype(str)
    )

    invalid_transaction_dependency = (
        ~valid_transactions["account_id"]
        .astype(str)
        .isin(valid_account_ids)
    )

    dependency_invalid_transactions = (
        valid_transactions[
            invalid_transaction_dependency
        ].copy()
    )

    valid_transactions = (
        valid_transactions[
            ~invalid_transaction_dependency
        ].copy()
    )


    # Add dependency-invalid transactions

    invalid_transactions = pd.concat(
        [
            invalid_transactions,
            dependency_invalid_transactions
        ],
        ignore_index=True
    )


    return (
        valid_accounts,
        valid_transactions,
        invalid_accounts,
        invalid_transactions
    )


# -----------------------------
# SAVE RESULTS
# -----------------------------

def save_results():

    (
        customers,
        accounts,
        transactions,
        issues
    ) = load_data()


    # -------------------------
    # DIRECT VALIDATION SPLIT
    # -------------------------

    valid_customers, invalid_customers = (
        get_invalid_rows(
            customers,
            "customers",
            issues
        )
    )

    valid_accounts, invalid_accounts = (
        get_invalid_rows(
            accounts,
            "accounts",
            issues
        )
    )

    valid_transactions, invalid_transactions = (
        get_invalid_rows(
            transactions,
            "transactions",
            issues
        )
    )


    # -------------------------
    # DEPENDENCY VALIDATION
    # -------------------------

    (
        valid_accounts,
        valid_transactions,
        invalid_accounts,
        invalid_transactions
    ) = apply_dependencies(
        valid_customers,
        valid_accounts,
        valid_transactions,
        invalid_accounts,
        invalid_transactions
    )


    # -------------------------
    # SAVE CLEANED DATA
    # -------------------------

    valid_customers.to_csv(
        CLEANED_DATA_DIR /
        "customers_cleaned.csv",
        index=False
    )

    valid_accounts.to_csv(
        CLEANED_DATA_DIR /
        "accounts_cleaned.csv",
        index=False
    )

    valid_transactions.to_csv(
        CLEANED_DATA_DIR /
        "transactions_cleaned.csv",
        index=False
    )


    # -------------------------
    # SAVE INVALID DATA
    # -------------------------

    invalid_customers.to_csv(
        INVALID_DATA_DIR /
        "customers_invalid.csv",
        index=False
    )

    invalid_accounts.to_csv(
        INVALID_DATA_DIR /
        "accounts_invalid.csv",
        index=False
    )

    invalid_transactions.to_csv(
        INVALID_DATA_DIR /
        "transactions_invalid.csv",
        index=False
    )


    # -------------------------
    # SUMMARY
    # -------------------------

    print("\n" + "=" * 55)

    print(
        "DEPENDENCY-AWARE DATA PROCESSING SUMMARY"
    )

    print("=" * 55)


    print("\nCUSTOMERS")

    print(
        f"Valid: {len(valid_customers)}"
    )

    print(
        f"Invalid: {len(invalid_customers)}"
    )


    print("\nACCOUNTS")

    print(
        f"Valid: {len(valid_accounts)}"
    )

    print(
        f"Invalid: {len(invalid_accounts)}"
    )


    print("\nTRANSACTIONS")

    print(
        f"Valid: {len(valid_transactions)}"
    )

    print(
        f"Invalid: {len(invalid_transactions)}"
    )


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    save_results()