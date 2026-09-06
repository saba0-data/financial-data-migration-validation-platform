-- ============================================
-- FINANCIAL DATA MIGRATION & VALIDATION PLATFORM
-- DATA RECONCILIATION QUERIES
-- ============================================


-- --------------------------------------------
-- 1. TARGET DATABASE RECORD COUNTS
-- --------------------------------------------

SELECT
    'customers' AS table_name,

    COUNT(*) AS record_count

FROM customers


UNION ALL


SELECT
    'accounts' AS table_name,

    COUNT(*) AS record_count

FROM accounts


UNION ALL


SELECT
    'transactions' AS table_name,

    COUNT(*) AS record_count

FROM transactions;


-- --------------------------------------------
-- 2. ACCOUNT BALANCE RECONCILIATION
-- --------------------------------------------

SELECT
    currency,

    COUNT(*) AS account_count,

    ROUND(
        SUM(balance),
        2
    ) AS total_balance

FROM accounts

GROUP BY
    currency

ORDER BY
    currency;


-- --------------------------------------------
-- 3. ACCOUNT SUMMARY BY TYPE
-- --------------------------------------------

SELECT
    account_type,

    COUNT(*) AS account_count,

    ROUND(
        SUM(balance),
        2
    ) AS total_balance

FROM accounts

GROUP BY
    account_type

ORDER BY
    total_balance DESC;


-- --------------------------------------------
-- 4. TRANSACTION AMOUNT RECONCILIATION
-- --------------------------------------------

SELECT
    transaction_type,

    COUNT(*) AS transaction_count,

    ROUND(
        SUM(amount),
        2
    ) AS total_amount

FROM transactions

GROUP BY
    transaction_type

ORDER BY
    total_amount DESC;


-- --------------------------------------------
-- 5. TRANSACTION CURRENCY SUMMARY
-- --------------------------------------------

SELECT
    currency,

    COUNT(*) AS transaction_count,

    ROUND(
        SUM(amount),
        2
    ) AS total_amount

FROM transactions

GROUP BY
    currency

ORDER BY
    currency;


-- --------------------------------------------
-- 6. TRANSACTION STATUS SUMMARY
-- --------------------------------------------

SELECT
    status,

    COUNT(*) AS transaction_count,

    ROUND(
        SUM(amount),
        2
    ) AS total_amount

FROM transactions

GROUP BY
    status

ORDER BY
    transaction_count DESC;


-- --------------------------------------------
-- 7. CUSTOMER TO ACCOUNT RECONCILIATION
-- --------------------------------------------

SELECT
    c.customer_id,
    c.full_name,

    COUNT(a.account_id) AS total_accounts,

    ROUND(
        COALESCE(SUM(a.balance), 0),
        2
    ) AS total_balance

FROM customers c

LEFT JOIN accounts a
    ON c.customer_id = a.customer_id

GROUP BY
    c.customer_id,
    c.full_name

ORDER BY
    total_balance DESC;


-- --------------------------------------------
-- 8. ACCOUNT TO TRANSACTION RECONCILIATION
-- --------------------------------------------

SELECT
    a.account_id,
    a.account_type,

    COUNT(t.transaction_id)
        AS total_transactions,

    ROUND(
        COALESCE(SUM(t.amount), 0),
        2
    ) AS total_transaction_amount

FROM accounts a

LEFT JOIN transactions t
    ON a.account_id = t.account_id

GROUP BY
    a.account_id,
    a.account_type

ORDER BY
    total_transaction_amount DESC;