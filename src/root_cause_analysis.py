import pandas as pd
from pathlib import Path


# -----------------------------
# PROJECT PATHS
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

REPORTS_DIR = BASE_DIR / "reports"

INPUT_REPORT = (
    REPORTS_DIR /
    "data_quality_report.csv"
)

OUTPUT_REPORT = (
    REPORTS_DIR /
    "root_cause_analysis_report.csv"
)


# -----------------------------
# RCA RULE MAPPING
# -----------------------------

RCA_MAPPING = {

    # CUSTOMER ISSUES

    "C01": {
        "root_cause": "Source system missing mandatory customer identifier",
        "impact": "Customer record cannot be uniquely identified",
        "remediation": "Populate customer ID from source system and enforce mandatory field validation",
        "priority": "High"
    },

    "C02": {
        "root_cause": "Duplicate customer identifier generated or received from source",
        "impact": "Duplicate customer records may cause incorrect account relationships",
        "remediation": "Identify duplicate source records and retain the approved master customer record",
        "priority": "High"
    },

    "C03": {
        "root_cause": "Mandatory email field missing in source data",
        "impact": "Customer contact information is incomplete",
        "remediation": "Retrieve missing email from source system or business owner",
        "priority": "Medium"
    },

    "C04": {
        "root_cause": "Email value does not follow expected format",
        "impact": "Invalid customer contact information",
        "remediation": "Correct email format and implement format validation in source system",
        "priority": "Medium"
    },

    "C05": {
        "root_cause": "Incorrect or future date received from source system",
        "impact": "Customer lifecycle timeline becomes unreliable",
        "remediation": "Correct source date and enforce date range validation",
        "priority": "High"
    },


    # ACCOUNT ISSUES

    "A01": {
        "root_cause": "Account record missing mandatory customer reference",
        "impact": "Account cannot be linked to a customer",
        "remediation": "Populate customer ID and enforce mandatory relationship validation",
        "priority": "High"
    },

    "A02": {
        "root_cause": "Duplicate account identifier generated or received from source",
        "impact": "Multiple records may represent the same financial account",
        "remediation": "Identify duplicate accounts and retain the approved account record",
        "priority": "High"
    },

    "A03": {
        "root_cause": "Customer reference does not exist in valid customer dataset",
        "impact": "Broken customer-to-account relationship",
        "remediation": "Correct customer reference or exclude account until valid parent record is available",
        "priority": "High"
    },

    "A04": {
        "root_cause": "Invalid negative balance received from source",
        "impact": "Financial reporting may be inaccurate",
        "remediation": "Investigate source balance and apply approved financial correction",
        "priority": "High"
    },

    "A05": {
        "root_cause": "Currency value is outside the approved domain",
        "impact": "Financial transactions may be incorrectly interpreted",
        "remediation": "Map currency to approved ISO currency code",
        "priority": "Medium"
    },

    "A06": {
        "root_cause": "Account type does not match approved business values",
        "impact": "Account classification becomes inconsistent",
        "remediation": "Map account type to approved business domain",
        "priority": "Medium"
    },

    "A07": {
        "root_cause": "Invalid future account opening date",
        "impact": "Account lifecycle information becomes inaccurate",
        "remediation": "Correct date using source system verification",
        "priority": "High"
    },


    # TRANSACTION ISSUES

    "T01": {
        "root_cause": "Transaction missing mandatory account reference",
        "impact": "Transaction cannot be linked to an account",
        "remediation": "Populate account ID or reject transaction until relationship is resolved",
        "priority": "High"
    },

    "T02": {
        "root_cause": "Duplicate transaction identifier generated or received from source",
        "impact": "Transaction may be counted multiple times",
        "remediation": "Identify duplicate transactions and retain approved transaction record",
        "priority": "High"
    },

    "T03": {
        "root_cause": "Account reference does not exist in valid account dataset",
        "impact": "Broken transaction-to-account relationship",
        "remediation": "Correct account reference or exclude transaction until valid account is available",
        "priority": "High"
    },

    "T04": {
        "root_cause": "Transaction amount is zero or negative",
        "impact": "Transaction value is invalid for migration",
        "remediation": "Verify transaction amount with source system and correct invalid value",
        "priority": "High"
    },

    "T05": {
        "root_cause": "Currency value is outside the approved domain",
        "impact": "Transaction currency cannot be interpreted correctly",
        "remediation": "Map currency to approved ISO currency code",
        "priority": "Medium"
    },

    "T06": {
        "root_cause": "Transaction type does not match approved business values",
        "impact": "Transaction classification becomes inconsistent",
        "remediation": "Map transaction type to approved business domain",
        "priority": "Medium"
    },

    "T07": {
        "root_cause": "Future transaction date received from source",
        "impact": "Transaction timeline becomes inaccurate",
        "remediation": "Verify and correct transaction date",
        "priority": "High"
    },

    "T08": {
        "root_cause": "Transaction status does not match approved business values",
        "impact": "Transaction processing state is inconsistent",
        "remediation": "Map status to approved transaction status",
        "priority": "Medium"
    }
}


# -----------------------------
# GENERATE RCA REPORT
# -----------------------------

def generate_rca_report():

    issues_df = pd.read_csv(
        INPUT_REPORT
    )

    rca_records = []

    for _, row in issues_df.iterrows():

        rule_id = row["rule_id"]

        mapping = RCA_MAPPING.get(
            rule_id,
            {
                "root_cause": "Unknown",
                "impact": "Requires investigation",
                "remediation": "Perform detailed root cause analysis",
                "priority": "Medium"
            }
        )

        rca_records.append({
            "table": row["table"],
            "row": row["row"],
            "rule_id": rule_id,
            "issue": row["issue"],
            "root_cause": mapping["root_cause"],
            "impact": mapping["impact"],
            "remediation": mapping["remediation"],
            "priority": mapping["priority"]
        })

    rca_df = pd.DataFrame(
        rca_records
    )

    rca_df.to_csv(
        OUTPUT_REPORT,
        index=False
    )

    return rca_df


# -----------------------------
# DISPLAY SUMMARY
# -----------------------------

def display_summary(rca_df):

    print("\n" + "=" * 55)

    print(
        "ROOT CAUSE ANALYSIS & REMEDIATION SUMMARY"
    )

    print("=" * 55)

    print(
        f"\nTotal Issues Analyzed: {len(rca_df)}"
    )

    print("\nIssues by Priority:")

    print(
        rca_df["priority"]
        .value_counts()
    )

    print("\nIssues by Table:")

    print(
        rca_df["table"]
        .value_counts()
    )

    print(
        "\nRCA Report Generated Successfully!"
    )


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    rca_df = generate_rca_report()

    display_summary(
        rca_df
    )

    print(
        "\nReport location:"
    )

    print(
        OUTPUT_REPORT
    )