-- ============================================
-- FINANCIAL DATA MIGRATION & VALIDATION PLATFORM
-- DATA QUALITY CHECKS
-- ============================================


-- ============================================
-- CUSTOMER DATA QUALITY CHECKS
-- ============================================


-- --------------------------------------------
-- 1. CUSTOMER MANDATORY FIELD CHECK
-- --------------------------------------------

SELECT *
FROM customers

WHERE customer_id IS NULL
   OR full_name IS NULL
   OR email IS NULL
   OR created_date IS NULL;


-- --------------------------------------------
-- 2. DUPLICATE CUSTOMER ID CHECK
-- --------------------------------------------

SELECT
    customer_id,

    COUNT(*) AS duplicate_count

FROM customers

GROUP BY
    customer_id

HAVING COUNT(*) > 1;


-- --------------------------------------------
-- 3. DUPLICATE CUSTOMER EMAIL CHECK
-- --------------------------------------------

SELECT
    email,

    COUNT(*) AS duplicate_count

FROM customers

GROUP BY
    email

HAVING COUNT(*) > 1;


-- --------------------------------------------
-- 4. INVALID EMAIL FORMAT CHECK
-- --------------------------------------------

SELECT *
FROM customers

WHERE email NOT LIKE '%@%.%';


-- --------------------------------------------
-- 5. FUTURE CUSTOMER CREATED DATE CHECK
-- --------------------------------------------

SELECT *
FROM customers

WHERE DATE(created_date) > DATE('now');


-- ============================================
-- ACCOUNT DATA QUALITY CHECKS
-- ============================================


-- --------------------------------------------
-- 6. ACCOUNT MANDATORY FIELD CHECK
-- --------------------------------------------

SELECT *
FROM accounts

WHERE account_id IS NULL
   OR customer_id IS NULL
   OR account_type IS NULL
   OR balance IS NULL
   OR currency IS NULL
   OR account_open_date IS NULL;


-- --------------------------------------------
-- 7. DUPLICATE ACCOUNT ID CHECK
-- --------------------------------------------

SELECT
    account_id,

    COUNT(*) AS duplicate_count

FROM accounts

GROUP BY
    account_id

HAVING COUNT(*) > 1;


-- --------------------------------------------
-- 8. INVALID ACCOUNT BALANCE CHECK
-- --------------------------------------------

SELECT *
FROM accounts

WHERE balance < 0;


-- --------------------------------------------
-- 9. INVALID CURRENCY CHECK
-- --------------------------------------------

SELECT *
FROM accounts

WHERE currency NOT IN (
    'USD',
    'INR',
    'EUR',
    'GBP'
);


-- --------------------------------------------
-- 10. INVALID ACCOUNT TYPE CHECK
-- --------------------------------------------

SELECT *
FROM accounts

WHERE account_type NOT IN (
    'Savings',
    'Current',
    'Salary',
    'Fixed Deposit'
);


-- --------------------------------------------
-- 11. FUTURE ACCOUNT OPEN DATE CHECK
-- --------------------------------------------

SELECT *
FROM accounts

WHERE DATE(account_open_date) > DATE('now');


-- ============================================
-- TRANSACTION DATA QUALITY CHECKS
-- ============================================


-- --------------------------------------------
-- 12. TRANSACTION MANDATORY FIELD CHECK
-- --------------------------------------------

SELECT *
FROM transactions

WHERE transaction_id IS NULL
   OR account_id IS NULL
   OR transaction_date IS NULL
   OR transaction_type IS NULL
   OR amount IS NULL
   OR currency IS NULL
   OR status IS NULL;


-- --------------------------------------------
-- 13. DUPLICATE TRANSACTION ID CHECK
-- --------------------------------------------

SELECT
    transaction_id,

    COUNT(*) AS duplicate_count

FROM transactions

GROUP BY
    transaction_id

HAVING COUNT(*) > 1;


-- --------------------------------------------
-- 14. INVALID TRANSACTION AMOUNT CHECK
-- --------------------------------------------

SELECT *
FROM transactions

WHERE amount <= 0;


-- --------------------------------------------
-- 15. INVALID TRANSACTION CURRENCY CHECK
-- --------------------------------------------

SELECT *
FROM transactions

WHERE currency NOT IN (
    'USD',
    'INR',
    'EUR',
    'GBP'
);


-- --------------------------------------------
-- 16. INVALID TRANSACTION TYPE CHECK
-- --------------------------------------------

SELECT *
FROM transactions

WHERE transaction_type NOT IN (
    'Credit',
    'Debit',
    'Transfer',
    'Payment'
);


-- --------------------------------------------
-- 17. FUTURE TRANSACTION DATE CHECK
-- --------------------------------------------

SELECT *
FROM transactions

WHERE DATE(transaction_date) > DATE('now');


-- --------------------------------------------
-- 18. INVALID TRANSACTION STATUS CHECK
-- --------------------------------------------

SELECT *
FROM transactions

WHERE status NOT IN (
    'Completed',
    'Pending',
    'Failed',
    'Cancelled'
);