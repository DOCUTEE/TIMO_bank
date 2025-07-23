WITH expense_trans_raw AS (
    SELECT 
        tl.transaction_id,
        a.customer_id,
        DATE(tl.transaction_time) AS txn_date,
        tl.transaction_time,
        tl.amount,
        al.auth_method,
        ROW_NUMBER() OVER (
            PARTITION BY tl.transaction_id
            ORDER BY al.auth_time
        ) AS row_num
    FROM transaction_log tl
    JOIN account a 
        ON tl.account_id = a.account_id
    JOIN auth_transaction at2 
        ON tl.transaction_id = at2.transaction_id
    JOIN authentication_log al 
        ON at2.auth_log_id = al.auth_log_id
    WHERE tl.transaction_type = 'expense'
),
expense_trans AS (
    SELECT * 
    FROM expense_trans_raw
    WHERE row_num = 1 
),
cumulative_expense_amount as (
	SELECT 
	    et.*,
	    SUM(et.amount) OVER (
	        PARTITION BY et.customer_id, et.txn_date
	        ORDER BY et.transaction_time
	    ) AS cumulative_expense
	FROM expense_trans et
	ORDER BY et.customer_id, et.transaction_time
),
over_20M_unuse_strong_auth as
(
	SELECT * 
	FROM cumulative_expense_amount cea
	WHERE cea.cumulative_expense > 20000000 and cea.auth_method != 'biometric'
)
select * 
from over_20M_unuse_strong_auth