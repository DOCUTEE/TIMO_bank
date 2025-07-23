with verified_device as
(
	Select * 
	from device
	where is_verified = true
),
authentication_for_verify as
(
	SELECT vd.device_id
	FROM 
		verified_device vd
		join
		authentication_log al
		on 
			vd.device_id = al.device_id and 
			used_for = 'device_verification'	
),
risky_authentication as
(
	SELECT * 
	FROM device dv
	WHERE dv.is_verified = true and dv.device_id not in (
		SELECT afv.device_id
		FROM authentication_for_verify afv
	)
)
SELECT * 
FROM risky_authentication
