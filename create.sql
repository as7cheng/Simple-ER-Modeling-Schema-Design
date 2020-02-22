DROP TABLE if exists Category;
CREATE TABLE Category
(
 category_id   INT          NOT NULL UNIQUE,
 category_name VARCHAR(255) NOT NULL UNIQUE,
 PRIMARY KEY (category_id)
);
 
DROP TABLE if exists Category;
CREATE TABLE Country 
(
 country_id   INT          NOT NULL UNIQUE,
 country_name VARCHAR(255) NOT NULL UNIQUE,
 PRIMARY KEY (country_id)
);
 
DROP TABLE if exists Location;
CREATE TABLE Location
(
 location_id INT          NOT NULL UNIQUE,
 location    VARCHAR(255) NOT NULL UNIQUE,
 country_id  INT,
 PRIMARY KEY (location_id),
 FOREIGN KEY (country_id) REFERENCES Country (country_id)
);

DROP TABLE if exists User;
CREATE TABLE User
(
 user_id     VARCHAR(255) NOT NULL UNIQUE,
 rating      INT          NOT NULL,
 location_id INT,
 PRIMARY KEY (user_id),
 FOREIGN KEY (location_id) REFERENCES Location (location_id)
);
 
DROP TABLE if exists Item;
CREATE TABLE Item
(
 item_id        INT          NOT NULL UNIQUE,
 name           VARCHAR(255) NOT NULL,
 currently      DOUBLE,
 buy_price      DOUBLE,
 first_bid      DOUBLE,
 number_of_bids INT          NOT NULL,
 location_id    INT          NOT NULL,
 started        datetime     NOT NULL,
 ends           datetime     NOT NULL,
 description    VARCHAR(255) NOT NULL,
 PRIMARY KEY (item_id),
 FOREIGN KEY (first_bid) REFERENCES Bid (bid_id),
 FOREIGN KEY (location_id) REFERENCES Location (location_id)
);
 
DROP TABLE if exists ItemCategory;
CREATE TABLE ItemCategory
(
 item_id     INT NOT NULL,
 category_id INT NOT NULL,
 PRIMARY KEY (item_id, category_id),
 FOREIGN KEY (item_id) REFERENCES Item (item_id),
 FOREIGN KEY (category_id) REFERENCES Category (category_id)
);


DROP TABLE if exists ItemSeller;
CREATE TABLE ItemSeller
(
 item_id   INT NOT NULL UNIQUE,
 seller_id VARCHAR(255) NOT NULL,
 PRIMARY KEY (item_id, seller_id),
 FOREIGN KEY (seller_id) REFERENCES USER (user_id)
);
 
DROP TABLE if exists Bid;
CREATE TABLE Bid
(
 bid_id    INT      NOT NULL UNIQUE,
 bidder_id VARCHAR(255)      NOT NULL,
 bid_time  datetime NOT NULL,
 amount    DOUBLE   NOT NULL,
 PRIMARY KEY (bid_id),
 FOREIGN KEY (bidder_id) REFERENCES USER (user_id)
);
 
DROP TABLE if exists ItemBid;
CREATE TABLE ItemBid
(
 item_id INT NOT NULL,
 bid_id  INT NOT NULL UNIQUE,
 PRIMARY KEY (bid_id),
 FOREIGN KEY (bid_id) REFERENCES Bid (bid_id),
 FOREIGN KEY (item_id) REFERENCES Item (item_id)
);
