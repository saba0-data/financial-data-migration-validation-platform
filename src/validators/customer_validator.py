import pandas as pd


def validate_customers(customers):

    issues = []

    # -------------------------
    # C01: Missing Customer ID
    # -------------------------

    invalid_rows = customers[
        customers["customer_id"].isna()
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "customers",
            "row": index,
            "rule_id": "C01",
            "issue": "Missing customer ID"
        })

    # -------------------------
    # C02: Duplicate Customer ID
    # -------------------------

    duplicate_rows = customers[
        customers["customer_id"].duplicated(
            keep=False
        )
        &
        customers["customer_id"].notna()
    ]

    for index, row in duplicate_rows.iterrows():

        issues.append({
            "table": "customers",
            "row": index,
            "rule_id": "C02",
            "issue": "Duplicate customer ID"
        })

    # -------------------------
    # C03: Missing Email
    # -------------------------

    invalid_rows = customers[
        customers["email"].isna()
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "customers",
            "row": index,
            "rule_id": "C03",
            "issue": "Missing email"
        })

    # -------------------------
    # C04: Invalid Email
    # -------------------------

    invalid_rows = customers[
        customers["email"].notna()
        &
        ~customers["email"].astype(str).str.contains(
            "@"
        )
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "customers",
            "row": index,
            "rule_id": "C04",
            "issue": "Invalid email format"
        })

    # -------------------------
    # C05: Future Created Date
    # -------------------------

    dates = pd.to_datetime(
        customers["created_date"],
        errors="coerce"
    )

    invalid_rows = customers[
        dates > pd.Timestamp.today()
    ]

    for index, row in invalid_rows.iterrows():

        issues.append({
            "table": "customers",
            "row": index,
            "rule_id": "C05",
            "issue": "Future created date"
        })

    return issues