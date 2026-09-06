import pandas as pd


VALID_CURRENCIES = [
    "INR",
    "USD",
    "EUR"
]

VALID_ACCOUNT_TYPES = [
    "Savings",
    "Current"
]


def validate_accounts(accounts, customers):

    issues = []

    # -------------------------
    # A01: Missing Customer ID
    # -------------------------

    invalid_rows = accounts[
        accounts["customer_id"].isna()
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "accounts",
            "row": index,
            "rule_id": "A01",
            "issue": "Missing customer ID"
        })

    # -------------------------
    # A02: Duplicate Account ID
    # -------------------------

    duplicate_rows = accounts[
        accounts["account_id"].duplicated(
            keep=False
        )
        &
        accounts["account_id"].notna()
    ]

    for index, row in duplicate_rows.iterrows():

        issues.append({
            "table": "accounts",
            "row": index,
            "rule_id": "A02",
            "issue": "Duplicate account ID"
        })

    # -------------------------
    # A03: Invalid Customer Reference
    # -------------------------

    valid_customer_ids = set(
        customers["customer_id"]
        .dropna()
        .astype(str)
    )

    invalid_rows = accounts[
        accounts["customer_id"].notna()
        &
        ~accounts["customer_id"]
        .astype(str)
        .isin(valid_customer_ids)
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "accounts",
            "row": index,
            "rule_id": "A03",
            "issue": "Invalid customer reference"
        })

    # -------------------------
    # A04: Negative Balance
    # -------------------------

    invalid_rows = accounts[
        accounts["balance"] < 0
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "accounts",
            "row": index,
            "rule_id": "A04",
            "issue": "Negative account balance"
        })

    # -------------------------
    # A05: Invalid Currency
    # -------------------------

    invalid_rows = accounts[
        ~accounts["currency"].isin(
            VALID_CURRENCIES
        )
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "accounts",
            "row": index,
            "rule_id": "A05",
            "issue": "Invalid currency"
        })

    # -------------------------
    # A06: Invalid Account Type
    # -------------------------

    invalid_rows = accounts[
        ~accounts["account_type"].isin(
            VALID_ACCOUNT_TYPES
        )
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "accounts",
            "row": index,
            "rule_id": "A06",
            "issue": "Invalid account type"
        })

    # -------------------------
    # A07: Future Account Date
    # -------------------------

    dates = pd.to_datetime(
        accounts["account_open_date"],
        errors="coerce"
    )

    invalid_rows = accounts[
        dates > pd.Timestamp.today()
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "accounts",
            "row": index,
            "rule_id": "A07",
            "issue": "Future account opening date"
        })

    return issues