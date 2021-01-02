-- Name: Joshua Kaiser, Timothy Yoon
-- Group: 57
-- Assignment: Project Step 6
-- File: data-definition-queries.sql
-- Description: This file contains data definition queries to
-- generate the database and insert queries to populate the
-- database with sample data.

CREATE DATABASE IF NOT EXISTS survivops;
USE survivops;


-- =============================================
-- Create table structures
-- =============================================

-- customers (Tim)

DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `customer_id` INT(255) AUTO_INCREMENT UNIQUE NOT NULL,
  `fname` VARCHAR(1000) NOT NULL,
  `lname` VARCHAR(1000) NOT NULL,
  `email` VARCHAR(1000) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phone_number` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- carts (Josh)

DROP TABLE IF EXISTS `carts`;
CREATE TABLE `carts` (
   `cart_id` INT(255) AUTO_INCREMENT not NULL PRIMARY KEY,
   `customer_id` INT(255),
   `cart_name` VARCHAR(1000) not NULL,
   FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- orders (Tim)

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `order_id` INT(255) AUTO_INCREMENT UNIQUE NOT NULL,
  `customer_id` INT(255),
  `billing_street` VARCHAR(1000) NOT NULL,
  `billing_city` VARCHAR(1000) NOT NULL,
  `billing_state` CHAR(2) NOT NULL,
  `billing_zip` VARCHAR(10) NOT NULL,
  `shipping_street` VARCHAR(1000),
  `shipping_city` VARCHAR(1000),
  `shipping_state` CHAR(2),
  `shipping_zip` VARCHAR(10),
  `shipped` BOOLEAN,
  `pickup_or_ship` BOOLEAN,
  `has_paid` BOOLEAN NOT NULL DEFAULT FALSE,
  `delivered` BOOLEAN NOT NULL DEFAULT FALSE,
  `order_date` DATETIME,
  PRIMARY KEY (`order_id`),
  FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- products (Josh)

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
   `product_id` INT(255) AUTO_INCREMENT not NULL PRIMARY KEY,
   `product_name` VARCHAR(1000) not NULL,
   `category` VARCHAR(1000) not NULL,
   `vendor` VARCHAR(1000) not NULL,
   `price` DECIMAL(18,2) not NULL,
   `image` VARCHAR(255),
   `quantity_available` INT(255) not NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- products_carts (Josh)

DROP TABLE IF EXISTS `products_carts`;
CREATE TABLE `products_carts` (
   `cart_id` INT(255) not NULL,
   `product_id` INT(255) not NULL,
   `product_quantity` INT(255) not NULL,
   PRIMARY KEY (`cart_id`, `product_id`),
   FOREIGN KEY (`cart_id`) REFERENCES `carts` (`cart_id`) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- products_orders (Tim)

DROP TABLE IF EXISTS `products_orders`;
CREATE TABLE `products_orders` (
   `order_id` INT(255) NOT NULL,
   `product_id` INT(255) NOT NULL,
   `product_quantity` INT(255) NOT NULL,
   PRIMARY KEY (`order_id`, `product_id`),
   FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- =============================================
-- Insert sample data into tables
-- =============================================

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
INSERT INTO `customers` (fname, lname, email, password, phone_number)
VALUES ('Gene', 'Fox', 'GeneLFox@dayrep.com', 'teeSe7lai', '336-650-5365'),
       ('Michael', 'Bormann', 'MichaelPBormann@armyspy.com', 'hee7Qui0t', '567-240-5343'),
       ('Devin', 'Drake', 'DevinMDrake@dayrep.com', 'HoetaaZia8ei', '254-616-0250'),
       ('Stephany', 'Lang', 'StephanyRLang@jourrapide.com', 'eimo2ohSh', '706-278-8529');
UNLOCK TABLES;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
INSERT INTO `carts` (customer_id, cart_name) VALUES 
(2, 'Kayak trip'),
(2, 'Ski trip'),
(1, 'Surf trip'),
(4, 'For Johns BDay');
UNLOCK TABLES;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
INSERT INTO `orders` (customer_id, billing_street, billing_city, billing_state, billing_zip, shipping_street, shipping_city, shipping_state, shipping_zip, shipped, pickup_or_ship, has_paid, delivered, order_date)
VALUES (1, '321 West Virginia Avenue', 'Albany', 'NY', '12210', '4045 Jacobs Street', 'Pittsburgh', 'PA', '15226', TRUE, TRUE, TRUE, TRUE, '2020-02-16 07:08:03'),
       (2, '4238 Strother Street', 'Birmingham', 'AL', '35203', '3317 Willow Greene Drive', 'Enterprise', 'AL', '36330', FALSE, TRUE, FALSE, FALSE, '2020-04-30 12:00:41'),
       (3, '1331 Havanna Street', 'Winston Salem', 'NC', '27101', '1809 Thomas Street', 'Libertyville', 'IL', '60048', FALSE, FALSE, TRUE, TRUE, '2020-05-28 08:13:38'),
       (4, '3049 Seth Street', 'Abilene', 'TX', '79602', '2379 Woodland Drive', 'Omaha', 'NE', '68102', TRUE, TRUE, TRUE, TRUE, '2020-03-30 23:41:18');
UNLOCK TABLES;

--
-- Data for products
--

LOCK TABLES `products` WRITE;
INSERT INTO `products` (product_name, category, vendor, price, quantity_available) VALUES 
('2-Person Tent', 'tents', 'patagonia', 578.99, 100),
('Kayak', 'boats', 'wilderness systems', 2000.00 ,2),
('backpack', 'backpacks', 'gregory', 200.00, 8),
('snow suit', 'apparel', 'north face', 400.00, 20);
UNLOCK TABLES;

--
-- Dumping data for table `products_carts`
--

LOCK TABLES `products_carts` WRITE;
INSERT INTO `products_carts` (cart_id, product_id, product_quantity) VALUES 
(1, 2, 9),
(2, 2, 18),
(1, 3, 2),
(3, 2, 1);
UNLOCK TABLES;

--
-- Dumping data for table `products_orders`
--

LOCK TABLES `products_orders` WRITE;
INSERT INTO `products_orders` (`order_id`, `product_id`, `product_quantity`)
VALUES (1, 3, 6),
       (2, 1, 1),
       (3, 4, 23),
       (4, 2, 0);
UNLOCK TABLES;
