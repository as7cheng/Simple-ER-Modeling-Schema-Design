SELECT COUNT(user_id)
	FROM User
	WHERE user_id IN (
    		SELECT seller_id
    		FROM ItemSeller
	) AND rating > 1000
