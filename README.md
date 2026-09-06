# Financial Data Migration & Validation Platform

## Project Overview

The Financial Data Migration & Validation Platform is an end-to-end data quality and ETL project designed to simulate the migration of financial data from source systems to a target database.

The project validates customer, account, and transaction data, identifies data quality issues, performs dependency-aware data cleansing, loads valid records into a SQLite database, and performs post-load reconciliation and SQL validation.

It also includes Root Cause Analysis (RCA) and an automated Excel Data Quality Dashboard for reporting and monitoring.

---

# Project Architecture

```text
Source Data
    │
    ▼
Data Generation
    │
    ▼
Data Issue Injection
    │
    ▼
Data Quality Validation
    │
    ▼
Dependency-Aware Data Processing
    │
    ├── Valid Data
    │
    └── Invalid Data
           │
           ▼
    Root Cause Analysis
    │
    ▼
ETL Data Loading
    │
    ▼
SQLite Database
    │
    ▼
Post-Load Validation
    │
    ▼
SQL Validation
    │
    ▼
Excel Data Quality Dashboard
```

---

# Key Features

- End-to-end financial data migration workflow
- Automated financial data generation
- Intentional data quality issue injection
- Rule-based data validation
- Data cleansing and segregation
- Dependency-aware data processing
- ETL data loading into SQLite
- Post-load validation and reconciliation
- SQL-based data validation
- Referential integrity checks
- Duplicate detection
- Root Cause Analysis (RCA)
- Automated Excel Data Quality Dashboard
- CSV-based validation and reporting
- Python automation

---

# Data Generation

The project generates realistic sample financial datasets for three core entities:

- Customers
- Bank Accounts
- Financial Transactions

## Records Generated

| Dataset | Records |
|---|---:|
| Customers | 100 |
| Accounts | 150 |
| Transactions | 500 |
| **Total** | **750** |

The generated data acts as the source system for the financial data migration pipeline.

---

# Data Quality Issue Injection

The project intentionally injects data quality issues into the generated datasets to simulate real-world data migration problems.

## Issues Introduced

### Customer Data Issues

- Missing customer information
- Invalid email values
- Duplicate records
- Data completeness issues
- Invalid customer data

### Account Data Issues

- Missing account information
- Invalid customer references
- Invalid account balances
- Invalid account attributes
- Data consistency issues

### Transaction Data Issues

- Missing transaction information
- Invalid account references
- Invalid transaction amounts
- Invalid transaction types
- Invalid transaction status
- Currency-related issues

This approach allows the validation pipeline to simulate realistic data quality problems before migration.

---

# Data Quality Validation

The project uses predefined validation rules to identify data quality issues across customer, account, and transaction datasets.

## Customer Validation

The validation process checks:

- Customer ID validation
- Missing value detection
- Email validation
- Duplicate detection
- Data completeness validation

## Account Validation

The validation process checks:

- Account ID validation
- Customer reference validation
- Account balance validation
- Account type validation
- Currency validation
- Data consistency validation

## Transaction Validation

The validation process checks:

- Transaction ID validation
- Account reference validation
- Transaction amount validation
- Transaction type validation
- Transaction status validation
- Currency validation
- Data consistency validation

All detected issues are documented in the data quality report.

---

# Dependency-Aware Data Processing

The project processes financial data based on relationships between datasets.

The dependency structure is:

```text
Customers
    │
    ▼
Accounts
    │
    ▼
Transactions
```

## Dependency Logic

A transaction depends on a valid account.

An account depends on a valid customer.

Therefore, invalid parent records can affect related child records.

For example:

```text
Invalid Customer
      │
      ▼
Related Account Cannot Be Migrated
      │
      ▼
Related Transactions Cannot Be Migrated
```

This dependency-aware processing helps maintain referential integrity during data migration.

The pipeline separates records into:

- Valid / Cleaned Data
- Invalid Data

---

# Data Processing Results

The dependency-aware data processing pipeline produced the following results.

| Metric | Result |
|---|---:|
| Total Source Records | 750 |
| Valid Records | 678 |
| Invalid Records | 72 |
| Migration Success Rate | 90.40% |

## Valid Records

| Dataset | Valid Records |
|---|---:|
| Customers | 94 |
| Accounts | 136 |
| Transactions | 448 |
| **Total** | **678** |

## Invalid Records

| Dataset | Invalid Records |
|---|---:|
| Customers | 6 |
| Accounts | 14 |
| Transactions | 52 |
| **Total** | **72** |

---

# ETL Data Loading

The project follows an ETL workflow to migrate validated financial data into a target database.

## ETL Workflow

```text
EXTRACT
   │
   ▼
Raw Source CSV Files
   │
   ▼
TRANSFORM
   │
   ├── Data Validation
   ├── Data Cleansing
   ├── Dependency Validation
   └── Invalid Record Segregation
   │
   ▼
LOAD
   │
   ▼
SQLite Target Database
```

Only validated records are loaded into the target database.

## Target Database

```text
data/database/financial_data.db
```

## Target Tables

The SQLite database contains:

- customers
- accounts
- transactions

The project uses SQLAlchemy for database interaction and SQLite for the target database.

---

# Post-Load Validation & Reconciliation

After loading the cleaned data into the target database, the project performs post-load validation and reconciliation.

## Validation Checks

The following checks are performed:

- Record count validation
- Column count validation
- Duplicate record validation
- Customer-to-account referential integrity validation
- Account-to-transaction referential integrity validation

## Post-Load Validation Results

| Metric | Result |
|---|---:|
| Total Checks | 11 |
| Passed | 11 |
| Failed | 0 |
| Success Rate | 100% |

The final validation confirmed that all migrated records were successfully loaded and that referential integrity was maintained.

---

# SQL Data Validation

The project performs additional validation using SQL queries against the SQLite target database.

## SQL Validation Checks

The SQL validation process checks:

1. Customer null values
2. Account null values
3. Transaction null values
4. Duplicate customers
5. Duplicate accounts
6. Duplicate transactions
7. Invalid account-to-customer references
8. Invalid transaction-to-account references

## SQL Validation Results

| Metric | Result |
|---|---:|
| Total SQL Checks | 8 |
| Passed | 8 |
| Failed | 0 |
| Success Rate | 100% |

SQL validation provides an additional layer of verification after the ETL loading process.

---

# Root Cause Analysis

The project includes a Root Cause Analysis (RCA) process for all identified data quality issues.

## RCA Includes

- Issue identification
- Issue categorization
- Priority classification
- Root cause identification
- Impact assessment
- Recommended remediation actions

## Priority Classification

Issues are categorized based on their severity:

- High
- Medium
- Low

## Root Cause Analysis Results

| Priority | Issues |
|---|---:|
| High | 21 |
| Medium | 7 |
| Low | 0 |
| **Total** | **28** |

The RCA report helps identify the underlying causes of data quality issues and supports future data quality improvements.

---

# Excel Data Quality Dashboard

The project automatically generates an Excel dashboard containing data migration and validation metrics.

## Dashboard Metrics

The dashboard includes:

- Total Source Records
- Valid Records
- Invalid Records
- Migration Success Rate
- Total Data Quality Issues
- Data Quality Issue Rate
- High Priority Issues
- Medium Priority Issues
- Low Priority Issues
- Post-Load Validation Results
- Post-Load Success Rate
- SQL Validation Results
- SQL Validation Success Rate
- Source vs Valid Record Comparison
- Issues by Table
- Issue Priority Distribution

## Dashboard Charts

The dashboard includes:

- Source vs Valid Records Bar Chart
- Issue Priority Distribution Chart

## Dashboard File

```text
reports/Financial_Data_Quality_Dashboard.xlsx
```

The dashboard also includes the following sheets:

1. Dashboard
2. Data Quality Issues
3. Root Cause Analysis
4. Post Load Validation
5. SQL Validation

---

# Project Structure

```text
financial-data-migration-validation-platform
│
├── data
│   │
│   ├── raw
│   │   ├── customers.csv
│   │   ├── accounts.csv
│   │   └── transactions.csv
│   │
│   ├── processed
│   │   ├── customers_with_issues.csv
│   │   ├── accounts_with_issues.csv
│   │   └── transactions_with_issues.csv
│   │
│   ├── cleaned
│   │   ├── customers_cleaned.csv
│   │   ├── accounts_cleaned.csv
│   │   └── transactions_cleaned.csv
│   │
│   ├── invalid
│   │   ├── customers_invalid.csv
│   │   ├── accounts_invalid.csv
│   │   └── transactions_invalid.csv
│   │
│   └── database
│       └── financial_data.db
│
├── reports
│   ├── screenshots
│   ├── data_quality_report.csv
│   ├── root_cause_analysis_report.csv
│   ├── post_load_validation_report.csv
│   ├── sql_validation_report.csv
│   └── Financial_Data_Quality_Dashboard.xlsx
│
├── sql
│
├── src
│   │
│   ├── validators
│   │
│   ├── generate_data.py
│   ├── inject_data_issues.py
│   ├── validation_engine.py
│   ├── data_processor.py
│   ├── etl_loader.py
│   ├── post_load_validation.py
│   ├── root_cause_analysis.py
│   ├── sql_validation.py
│   └── excel_dashboard.py
│
├── tests
│
├── config
│
├── docs
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Technologies Used

## Programming Language

- Python 3

## Data Processing

- Pandas
- NumPy

## Database

- SQLite
- SQLAlchemy

## Data Validation

- Python Validation Rules
- SQL Validation
- Referential Integrity Checks
- Duplicate Detection
- Null Value Validation

## Data Generation

- Faker

## Reporting

- Microsoft Excel
- OpenPyXL
- CSV Reports

## Development Tools

- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/saba0-data/financial-data-migration-validation-platform.git
```

## 2. Navigate to the Project Directory

```bash
cd financial-data-migration-validation-platform
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

## 4. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

## 5. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

Run the project scripts in the following order.

## Step 1: Generate Financial Data

```bash
python src/generate_data.py
```

This generates:

- 100 customer records
- 150 account records
- 500 transaction records

---

## Step 2: Inject Data Quality Issues

```bash
python src/inject_data_issues.py
```

This intentionally introduces data quality problems into the datasets.

---

## Step 3: Run Data Quality Validation

```bash
python src/validation_engine.py
```

This identifies data quality issues and generates:

```text
reports/data_quality_report.csv
```

---

## Step 4: Process Valid and Invalid Data

```bash
python src/data_processor.py
```

This performs dependency-aware processing and separates data into:

- Cleaned Data
- Invalid Data

---

## Step 5: Load Valid Data into SQLite

```bash
python src/etl_loader.py
```

This loads cleaned financial data into:

```text
data/database/financial_data.db
```

---

## Step 6: Perform Post-Load Validation

```bash
python src/post_load_validation.py
```

This validates:

- Record counts
- Column counts
- Duplicate records
- Referential integrity

---

## Step 7: Perform Root Cause Analysis

```bash
python src/root_cause_analysis.py
```

This analyzes data quality issues and generates remediation information.

---

## Step 8: Run SQL Validation

```bash
python src/sql_validation.py
```

This performs SQL-based validation against the target database.

---

## Step 9: Generate Excel Dashboard

```bash
python src/excel_dashboard.py
```

This generates:

```text
reports/Financial_Data_Quality_Dashboard.xlsx
```

---

# Validation Reports

The project automatically generates multiple validation and reporting files.

## Data Quality Report

```text
reports/data_quality_report.csv
```

Contains:

- Data quality issues
- Validation rules
- Affected records
- Issue categories

---

## Root Cause Analysis Report

```text
reports/root_cause_analysis_report.csv
```

Contains:

- Issue information
- Priority
- Root cause
- Recommended remediation

---

## Post-Load Validation Report

```text
reports/post_load_validation_report.csv
```

Contains:

- Record count validation
- Column validation
- Duplicate checks
- Referential integrity checks
- Validation status

---

## SQL Validation Report

```text
reports/sql_validation_report.csv
```

Contains:

- SQL validation name
- Issue count
- Validation status

---

## Excel Data Quality Dashboard

```text
reports/Financial_Data_Quality_Dashboard.xlsx
```

Contains:

- Executive dashboard
- Data Quality Issues
- Root Cause Analysis
- Post Load Validation
- SQL Validation

---

# Key Learnings

This project demonstrates practical experience with:

- Financial Data Management
- Data Migration
- Data Quality Management
- Data Validation
- Data Cleansing
- ETL Processes
- Data Integration
- SQL Validation
- Database Loading
- Data Reconciliation
- Post-Load Validation
- Referential Integrity
- Dependency-Aware Data Processing
- Root Cause Analysis
- Data Defect Investigation
- CSV Processing
- SQLite
- SQLAlchemy
- Pandas
- Excel Dashboard Automation
- Python Automation

---

# Business Value

The platform simulates a real-world financial data migration process and provides several business benefits.

## Improved Data Quality

Identifies data quality issues before records are migrated to the target system.

## Reduced Migration Risk

Prevents invalid and inconsistent records from entering the target database.

## Referential Integrity

Maintains valid relationships between:

```text
Customers
    ↓
Accounts
    ↓
Transactions
```

## Automated Validation

Reduces manual validation effort through automated Python and SQL checks.

## Better Issue Investigation

Root Cause Analysis helps identify the underlying causes of data defects.

## Improved Reporting

The automated Excel dashboard provides a clear summary of:

- Data quality
- Migration success
- Validation results
- Issue priorities

## Reusable Data Pipeline

The project structure can be extended to support larger datasets and additional data sources.

---

# Future Improvements

Potential future enhancements include:

## Cloud Integration

- Azure Data Factory
- Azure SQL Database
- Azure Blob Storage

## Enterprise ETL Integration

- SAP BusinessObjects Data Services (SAP BODS)
- Additional ETL workflows

## Dashboard Improvements

- Streamlit Web Dashboard
- Power BI Dashboard
- Interactive Data Quality Monitoring

## Automation

- Scheduled pipeline execution
- Automated data quality alerts
- Email notifications

## Testing

- Unit testing
- Integration testing
- Automated validation tests

## Data Quality Enhancements

- Data quality scoring
- Data profiling
- Advanced anomaly detection
- Automated remediation

## Database Improvements

- PostgreSQL
- SQL Server
- Cloud database integration

## CI/CD

- GitHub Actions
- Automated testing pipelines
- Automated deployment

---

# Skills Demonstrated

This project demonstrates skills relevant to Data Management, Data Validation, ETL, and Data Quality roles.

### Technical Skills

- Python
- SQL
- Pandas
- SQLAlchemy
- SQLite
- OpenPyXL
- ETL
- Data Validation
- Data Cleansing
- Data Migration
- Data Reconciliation
- Root Cause Analysis

### Data Management Skills

- Data Quality Management
- Data Integrity
- Referential Integrity
- Data Defect Investigation
- Post-Load Validation
- Dependency Management
- Data Issue Reporting

### Reporting Skills

- Excel Dashboard Creation
- Automated Reporting
- Data Quality Reporting
- Validation Reports

---

# Author

**Saba Sulthana**

GitHub:  
https://github.com/saba0-data

---

# License

This project is created for educational and portfolio purposes.
