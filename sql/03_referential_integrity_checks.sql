-- ============================================
-- FINANCIAL DATA MIGRATION & VALIDATION PLATFORM
-- REFERENTIAL INTEGRITY CHECKS
-- ============================================


-- --------------------------------------------
-- 1. ACCOUNTS WITHOUT VALID CUSTOMERS
-- --------------------------------------------

SELECT
    a.account_id,
    a.customer_id,
    a.account_type,
    a.balance

FROM accounts a

LEFT JOIN customers c
    ON a.customer_id = c.customer_id

WHERE c.customer_id IS NULL;


-- --------------------------------------------
-- 2. TRANSACTIONS WITHOUT VALID ACCOUNTS
-- --------------------------------------------

SELECT
    t.transaction_id,
    t.account_id,
    t.transaction_type,
    t.amount

FROM transactions t

LEFT JOIN accounts a
    ON t.account_id = a.account_id

WHERE a.account_id IS NULL;


-- --------------------------------------------
-- 3. CUSTOMER ACCOUNT RELATIONSHIP SUMMARY
-- --------------------------------------------

SELECT
    c.customer_id,
    c.full_name,

    COUNT(a.account_id) AS account_count

FROM customers c

LEFT JOIN accounts a
    ON c.customer_id = a.customer_id

GROUP BY
    c.customer_id,
    c.full_name

ORDER BY
    account_count DESC;


-- --------------------------------------------
-- 4. ACCOUNT TRANSACTION RELATIONSHIP SUMMARY
-- --------------------------------------------

SELECT
    a.account_id,
    a.account_type,

    COUNT(t.transaction_id)
        AS transaction_count

FROM accounts a

LEFT JOIN transactions t
    ON a.account_id = t.account_id

GROUP BY
    a.account_id,
    a.account_type

ORDER BY
    transaction_count DESC;


-- --------------------------------------------
-- 5. CUSTOMERS WITHOUT ACCOUNTS
-- --------------------------------------------

SELECT
    c.customer_id,
    c.full_name,
    c.email

FROM customers c

LEFT JOIN accounts a
    ON c.customer_id = a.customer_id

WHERE a.account_id IS NULL;


-- --------------------------------------------
-- 6. ACCOUNTS WITHOUT TRANSACTIONS
-- --------------------------------------------

SELECT
    a.account_id,
    a.customer_id,
    a.account_type,
    a.balance

FROM accounts a

LEFT JOIN transactions t
    ON a.account_id = t.account_id

WHERE t.transaction_id IS NULL;