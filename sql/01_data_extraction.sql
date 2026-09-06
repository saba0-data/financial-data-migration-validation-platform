-- ============================================
-- FINANCIAL DATA MIGRATION & VALIDATION PLATFORM
-- DATA EXTRACTION QUERIES
-- ============================================


-- --------------------------------------------
-- 1. VIEW ALL CUSTOMERS
-- --------------------------------------------

SELECT
    customer_id,
    full_name,
    email,
    phone,
    city,
    created_date
FROM customers;


-- --------------------------------------------
-- 2. VIEW ALL ACCOUNTS
-- --------------------------------------------

SELECT
    account_id,
    customer_id,
    account_type,
    balance,
    currency,
    account_open_date
FROM accounts;


-- --------------------------------------------
-- 3. VIEW ALL TRANSACTIONS
-- --------------------------------------------

SELECT
    transaction_id,
    account_id,
    transaction_date,
    transaction_type,
    amount,
    currency,
    status
FROM transactions;


-- --------------------------------------------
-- 4. CUSTOMER ACCOUNT SUMMARY
-- --------------------------------------------

SELECT
    c.customer_id,
    c.full_name,
    c.email,

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
    c.full_name,
    c.email

ORDER BY
    total_balance DESC;


-- --------------------------------------------
-- 5. ACCOUNT SUMMARY BY TYPE
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
-- 6. ACCOUNT SUMMARY BY CURRENCY
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
    total_balance DESC;


-- --------------------------------------------
-- 7. TRANSACTION SUMMARY BY TYPE
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
-- 8. TRANSACTION SUMMARY BY STATUS
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
-- 9. CUSTOMER ACCOUNT DETAILS
-- --------------------------------------------

SELECT
    c.customer_id,
    c.full_name,
    c.city,

    a.account_id,
    a.account_type,
    a.balance,
    a.currency,
    a.account_open_date

FROM customers c

INNER JOIN accounts a
    ON c.customer_id = a.customer_id

ORDER BY
    c.customer_id,
    a.account_id;


-- --------------------------------------------
-- 10. ACCOUNT TRANSACTION DETAILS
-- --------------------------------------------

SELECT
    a.account_id,
    a.account_type,
    a.balance,

    t.transaction_id,
    t.transaction_date,
    t.transaction_type,
    t.amount,
    t.currency,
    t.status

FROM accounts a

INNER JOIN transactions t
    ON a.account_id = t.account_id

ORDER BY
    a.account_id,
    t.transaction_date;