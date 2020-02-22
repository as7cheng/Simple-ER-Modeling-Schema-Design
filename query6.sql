SELECT COUNT(DISTINCT seller_id) 
	FROM ItemSeller 
	WHERE seller_id IN (SELECT DISTINCT bidder_id 
				FROM Bid)
