SELECT COUNT(item_id) 
	FROM (SELECT item_id, COUNT(category_id) AS num 
		FROM ItemCategory 
		GROUP BY item_id) 
	WHERE num = 4;
