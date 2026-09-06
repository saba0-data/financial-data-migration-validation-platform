import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text


# -----------------------------
# PROJECT PATHS
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CLEANED_DATA_DIR = BASE_DIR / "data" / "cleaned"

DATABASE_PATH = (
    BASE_DIR /
    "database" /
    "financial_data.db"
)

REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# -----------------------------
# LOAD SOURCE DATA
# -----------------------------

def load_source_data():

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

    return {
        "customers": customers,
        "accounts": accounts,
        "transactions": transactions
    }


# -----------------------------
# LOAD TARGET DATA
# -----------------------------

def load_target_data():

    customers = pd.read_sql(
        "SELECT * FROM customers",
        engine
    )

    accounts = pd.read_sql(
        "SELECT * FROM accounts",
        engine
    )

    transactions = pd.read_sql(
        "SELECT * FROM transactions",
        engine
    )

    return {
        "customers": customers,
        "accounts": accounts,
        "transactions": transactions
    }


# -----------------------------
# RECORD COUNT VALIDATION
# -----------------------------

def validate_record_counts(
    source_data,
    target_data
):

    results = []

    for table in source_data:

        source_count = len(
            source_data[table]
        )

        target_count = len(
            target_data[table]
        )

        status = (
            "PASS"
            if source_count == target_count
            else "FAIL"
        )

        results.append({
            "validation_type": "Record Count",
            "table": table,
            "source_value": source_count,
            "target_value": target_count,
            "status": status
        })

    return results


# -----------------------------
# COLUMN VALIDATION
# -----------------------------

def validate_columns(
    source_data,
    target_data
):

    results = []

    for table in source_data:

        source_columns = set(
            source_data[table].columns
        )

        target_columns = set(
            target_data[table].columns
        )

        status = (
            "PASS"
            if source_columns == target_columns
            else "FAIL"
        )

        results.append({
            "validation_type": "Column Check",
            "table": table,
            "source_value": len(source_columns),
            "target_value": len(target_columns),
            "status": status
        })

    return results


# -----------------------------
# PRIMARY KEY DUPLICATE CHECK
# -----------------------------

def validate_duplicates(target_data):

    results = []

    primary_keys = {
        "customers": "customer_id",
        "accounts": "account_id",
        "transactions": "transaction_id"
    }

    for table, primary_key in primary_keys.items():

        duplicate_count = (
            target_data[table][primary_key]
            .duplicated()
            .sum()
        )

        status = (
            "PASS"
            if duplicate_count == 0
            else "FAIL"
        )

        results.append({
            "validation_type": "Duplicate Check",
            "table": table,
            "source_value": 0,
            "target_value": duplicate_count,
            "status": status
        })

    return results


# -----------------------------
# REFERENTIAL INTEGRITY CHECK
# -----------------------------

def validate_referential_integrity(
    target_data
):

    results = []

    # Accounts → Customers

    valid_customer_ids = set(
        target_data["customers"]
        ["customer_id"]
    )

    invalid_account_refs = (
        ~target_data["accounts"]
        ["customer_id"]
        .isin(valid_customer_ids)
    ).sum()

    status = (
        "PASS"
        if invalid_account_refs == 0
        else "FAIL"
    )

    results.append({
        "validation_type":
            "Referential Integrity",
        "table":
            "accounts → customers",
        "source_value": 0,
        "target_value":
            invalid_account_refs,
        "status": status
    })


    # Transactions → Accounts

    valid_account_ids = set(
        target_data["accounts"]
        ["account_id"]
    )

    invalid_transaction_refs = (
        ~target_data["transactions"]
        ["account_id"]
        .isin(valid_account_ids)
    ).sum()

    status = (
        "PASS"
        if invalid_transaction_refs == 0
        else "FAIL"
    )

    results.append({
        "validation_type":
            "Referential Integrity",
        "table":
            "transactions → accounts",
        "source_value": 0,
        "target_value":
            invalid_transaction_refs,
        "status": status
    })

    return results


# -----------------------------
# SAVE RECONCILIATION REPORT
# -----------------------------

def save_report(results):

    results_df = pd.DataFrame(
        results
    )

    report_path = (
        REPORTS_DIR /
        "post_load_validation_report.csv"
    )

    results_df.to_csv(
        report_path,
        index=False
    )

    return results_df


# -----------------------------
# DISPLAY SUMMARY
# -----------------------------

def display_summary(results_df):

    print("\n" + "=" * 55)

    print(
        "POST-LOAD VALIDATION "
        "& RECONCILIATION SUMMARY"
    )

    print("=" * 55)

    print(
        "\nTotal Checks: "
        f"{len(results_df)}"
    )

    print(
        "Passed: "
        f"{len(results_df[results_df['status'] == 'PASS'])}"
    )

    print(
        "Failed: "
        f"{len(results_df[results_df['status'] == 'FAIL'])}"
    )

    print("\nValidation Results:\n")

    print(
        results_df.to_string(
            index=False
        )
    )


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    print(
        "\nLoading source data..."
    )

    source_data = load_source_data()


    print(
        "Loading target data..."
    )

    target_data = load_target_data()


    results = []

    print(
        "Running record count validation..."
    )

    results.extend(
        validate_record_counts(
            source_data,
            target_data
        )
    )


    print(
        "Running column validation..."
    )

    results.extend(
        validate_columns(
            source_data,
            target_data
        )
    )


    print(
        "Running duplicate checks..."
    )

    results.extend(
        validate_duplicates(
            target_data
        )
    )


    print(
        "Running referential integrity checks..."
    )

    results.extend(
        validate_referential_integrity(
            target_data
        )
    )


    results_df = save_report(
        results
    )

    display_summary(
        results_df
    )

    print(
        "\nReport saved successfully:"
    )

    print(
        REPORTS_DIR /
        "post_load_validation_report.csv"
    )