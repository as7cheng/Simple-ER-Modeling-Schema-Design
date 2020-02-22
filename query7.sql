SELECT COUNT(DISTINCT category_id) 
    FROM ItemCategory
    WHERE item_id IN(
        	SELECT item_id 
        		FROM ItemBid 
        		WHERE bid_id IN (
            			SELECT bid_id 
            				FROM Bid 
            				WHERE amount > 100
       			 )
    )
