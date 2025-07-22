with transaction_joined as
(
	SELECT
		tl.transaction_id,
		tl.amount,		
		tl.status,
		a.auth_method,
		a.is_strong
	FROM 
		auth_transaction at join
		transaction_log tl
			on at.transaction_id = tl.transaction_id
		join authentication_log al
			on at.auth_log_id = al.auth_log_id
		join authentication a 
			on al.auth_method = a.auth_method
	WHERE 
		tl.transaction_type = 'expense'
),
over_10M as
(
	SELECT 
		tj.*
	FROM
		transaction_joined tj
	Where 
		tj.amount > 10000000
	GROUP BY tj.transaction_id
	having 
		SUM(CASE WHEN tj.is_strong = TRUE THEN 1 ELSE 0 END) = 0
	ORDER BY tj.transaction_id 
)
select * 
from over_10M