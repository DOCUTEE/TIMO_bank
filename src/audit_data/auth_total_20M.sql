WITH expense_txns AS (
    SELECT 
        tl.transaction_id,
        a.customer_id,
        DATE(tl.transaction_time) AS txn_date,
        tl.transaction_time,
        tl.amount,
        al.auth_method
    FROM transaction_log tl
    JOIN account a ON tl.account_id = a.account_id
    JOIN auth_transaction at2 ON tl.transaction_id = at2.transaction_id
    JOIN authentication_log al ON at2.auth_log_id = al.auth_log_id
    WHERE tl.transaction_type = 'expense'
),
running_total AS (
    SELECT 
        transaction_id,
        customer_id,
        txn_date,
        transaction_time,
        amount,
        auth_method,
        SUM(amount) OVER (
            PARTITION BY customer_id, txn_date
            ORDER BY transaction_time
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_sum
    FROM expense_txns
),
flagged_transactions AS (
    SELECT 
        rt.transaction_id,
        rt.customer_id,
        rt.txn_date,
        rt.transaction_time,
        rt.amount,
        rt.auth_method,
        rt.running_sum,
        CASE 
            WHEN rt.running_sum >= 20000000 THEN 1
            ELSE 0
        END AS needs_biometric
    FROM running_total rt
),
violations AS (
    SELECT *
    FROM flagged_transactions
    WHERE needs_biometric = 1
    GROUP BY transaction_id
    HAVING SUM(CASE WHEN auth_method = 'biometric' THEN 1 ELSE 0 END) = 0
)
SELECT 
    customer_id,
    txn_date,
    transaction_id,
    transaction_time,
    amount,
    running_sum
FROM violations
ORDER BY customer_id, txn_date, transaction_time;
