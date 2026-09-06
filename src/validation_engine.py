import pandas as pd
from pathlib import Path

from validators.customer_validator import validate_customers
from validators.account_validator import validate_accounts
from validators.transaction_validator import validate_transactions


# -----------------------------
# PROJECT PATHS
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(
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

    return customers, accounts, transactions


# -----------------------------
# RUN VALIDATIONS
# -----------------------------

def run_validations():

    customers, accounts, transactions = load_data()

    all_issues = []

    print("\nRunning customer validations...")

    customer_issues = validate_customers(
        customers
    )

    all_issues.extend(
        customer_issues
    )

    print(
        f"Customer issues found: "
        f"{len(customer_issues)}"
    )


    print("\nRunning account validations...")

    account_issues = validate_accounts(
        accounts,
        customers
    )

    all_issues.extend(
        account_issues
    )

    print(
        f"Account issues found: "
        f"{len(account_issues)}"
    )


    print("\nRunning transaction validations...")

    transaction_issues = validate_transactions(
        transactions,
        accounts
    )

    all_issues.extend(
        transaction_issues
    )

    print(
        f"Transaction issues found: "
        f"{len(transaction_issues)}"
    )


    return all_issues


# -----------------------------
# SAVE VALIDATION REPORT
# -----------------------------

def save_report(issues):

    issues_df = pd.DataFrame(
        issues
    )

    report_path = (
        REPORTS_DIR /
        "data_quality_report.csv"
    )

    issues_df.to_csv(
        report_path,
        index=False
    )

    print(
        "\nValidation report saved:"
    )

    print(report_path)

    return issues_df


# -----------------------------
# DISPLAY SUMMARY
# -----------------------------

def display_summary(issues_df):

    print("\n" + "=" * 50)

    print("DATA QUALITY VALIDATION SUMMARY")

    print("=" * 50)

    print(
        f"\nTotal Issues Found: "
        f"{len(issues_df)}"
    )

    print("\nIssues by Table:")

    print(
        issues_df["table"]
        .value_counts()
    )

    print("\nIssues by Rule:")

    print(
        issues_df["rule_id"]
        .value_counts()
    )


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    issues = run_validations()

    issues_df = save_report(
        issues
    )

    display_summary(
        issues_df
    )