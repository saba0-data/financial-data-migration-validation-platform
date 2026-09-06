import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text


# -----------------------------
# PROJECT PATHS
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

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
# SQL VALIDATION QUERIES
# -----------------------------

VALIDATION_QUERIES = {

    # -------------------------
    # NULL CHECKS
    # -------------------------

    "customers_null_check": """
        SELECT COUNT(*) AS issue_count
        FROM customers
        WHERE customer_id IS NULL
           OR full_name IS NULL
           OR email IS NULL
           OR created_date IS NULL
    """,

    "accounts_null_check": """
        SELECT COUNT(*) AS issue_count
        FROM accounts
        WHERE account_id IS NULL
           OR customer_id IS NULL
           OR account_type IS NULL
           OR balance IS NULL
           OR currency IS NULL
    """,

    "transactions_null_check": """
        SELECT COUNT(*) AS issue_count
        FROM transactions
        WHERE transaction_id IS NULL
           OR account_id IS NULL
           OR transaction_date IS NULL
           OR transaction_type IS NULL
           OR amount IS NULL
           OR currency IS NULL
           OR status IS NULL
    """,


    # -------------------------
    # DUPLICATE CHECKS
    # -------------------------

    "duplicate_customers": """
        SELECT COUNT(*) AS issue_count
        FROM (
            SELECT customer_id
            FROM customers
            GROUP BY customer_id
            HAVING COUNT(*) > 1
        )
    """,

    "duplicate_accounts": """
        SELECT COUNT(*) AS issue_count
        FROM (
            SELECT account_id
            FROM accounts
            GROUP BY account_id
            HAVING COUNT(*) > 1
        )
    """,

    "duplicate_transactions": """
        SELECT COUNT(*) AS issue_count
        FROM (
            SELECT transaction_id
            FROM transactions
            GROUP BY transaction_id
            HAVING COUNT(*) > 1
        )
    """,


    # -------------------------
    # REFERENTIAL INTEGRITY
    # -------------------------

    "invalid_account_customer_reference": """
        SELECT COUNT(*) AS issue_count
        FROM accounts a
        LEFT JOIN customers c
            ON a.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """,

    "invalid_transaction_account_reference": """
        SELECT COUNT(*) AS issue_count
        FROM transactions t
        LEFT JOIN accounts a
            ON t.account_id = a.account_id
        WHERE a.account_id IS NULL
    """
}


# -----------------------------
# RUN SQL VALIDATIONS
# -----------------------------

def run_sql_validations():

    results = []

    with engine.connect() as connection:

        for validation_name, query in (
            VALIDATION_QUERIES.items()
        ):

            result = connection.execute(
                text(query)
            )

            issue_count = (
                result.fetchone()[0]
            )

            status = (
                "PASS"
                if issue_count == 0
                else "FAIL"
            )

            results.append({
                "validation_name":
                    validation_name,
                "issue_count":
                    issue_count,
                "status":
                    status
            })

    return pd.DataFrame(results)


# -----------------------------
# DISPLAY RESULTS
# -----------------------------

def display_results(results_df):

    total_checks = len(results_df)

    passed_checks = len(
        results_df[
            results_df["status"] == "PASS"
        ]
    )

    failed_checks = len(
        results_df[
            results_df["status"] == "FAIL"
        ]
    )


    print("\n" + "=" * 60)

    print(
        "SQL DATA VALIDATION SUMMARY"
    )

    print("=" * 60)

    print(
        "\nValidation Results:\n"
    )

    print(
        results_df.to_string(
            index=False
        )
    )


    print("\n" + "-" * 60)

    print(
        f"Total Checks: {total_checks}"
    )

    print(
        f"Passed: {passed_checks}"
    )

    print(
        f"Failed: {failed_checks}"
    )


# -----------------------------
# SAVE REPORT
# -----------------------------

def save_report(results_df):

    report_path = (
        REPORTS_DIR /
        "sql_validation_report.csv"
    )

    results_df.to_csv(
        report_path,
        index=False
    )

    print(
        "\nSQL Validation Report Saved:"
    )

    print(
        report_path
    )


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    results_df = run_sql_validations()

    display_results(
        results_df
    )

    save_report(
        results_df
    )