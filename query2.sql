SELECT COUNT(*) 
	FROM User 
	WHERE location_id IN (SELECT location_id 
					FROM location 
					WHERE location = "New York");
