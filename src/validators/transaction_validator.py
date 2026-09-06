import pandas as pd


VALID_CURRENCIES = [
    "INR",
    "USD",
    "EUR"
]

VALID_TRANSACTION_TYPES = [
    "Credit",
    "Debit"
]

VALID_STATUS = [
    "Completed",
    "Pending",
    "Failed"
]


def validate_transactions(transactions, accounts):

    issues = []

    # -------------------------
    # T01: Missing Account ID
    # -------------------------

    invalid_rows = transactions[
        transactions["account_id"].isna()
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T01",
            "issue": "Missing account ID"
        })

    # -------------------------
    # T02: Duplicate Transaction ID
    # -------------------------

    duplicate_rows = transactions[
        transactions["transaction_id"]
        .duplicated(keep=False)
        &
        transactions["transaction_id"].notna()
    ]

    for index, row in duplicate_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T02",
            "issue": "Duplicate transaction ID"
        })

    # -------------------------
    # T03: Invalid Account Reference
    # -------------------------

    valid_account_ids = set(
        accounts["account_id"]
        .dropna()
        .astype(str)
    )

    invalid_rows = transactions[
        transactions["account_id"].notna()
        &
        ~transactions["account_id"]
        .astype(str)
        .isin(valid_account_ids)
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T03",
            "issue": "Invalid account reference"
        })

    # -------------------------
    # T04: Invalid Amount
    # -------------------------

    invalid_rows = transactions[
        transactions["amount"] <= 0
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T04",
            "issue": "Transaction amount must be greater than zero"
        })

    # -------------------------
    # T05: Invalid Currency
    # -------------------------

    invalid_rows = transactions[
        ~transactions["currency"].isin(
            VALID_CURRENCIES
        )
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T05",
            "issue": "Invalid currency"
        })

    # -------------------------
    # T06: Invalid Transaction Type
    # -------------------------

    invalid_rows = transactions[
        ~transactions["transaction_type"].isin(
            VALID_TRANSACTION_TYPES
        )
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T06",
            "issue": "Invalid transaction type"
        })

    # -------------------------
    # T07: Future Transaction Date
    # -------------------------

    dates = pd.to_datetime(
        transactions["transaction_date"],
        errors="coerce"
    )

    invalid_rows = transactions[
        dates > pd.Timestamp.today()
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T07",
            "issue": "Future transaction date"
        })

    # -------------------------
    # T08: Invalid Status
    # -------------------------

    invalid_rows = transactions[
        ~transactions["status"].isin(
            VALID_STATUS
        )
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "transactions",
            "row": index,
            "rule_id": "T08",
            "issue": "Invalid transaction status"
        })

    return issues