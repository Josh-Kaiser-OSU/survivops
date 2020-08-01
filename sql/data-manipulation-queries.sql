-- Name: Joshua Kaiser, Timothy Yoon
-- Group: 57
-- Assignment: Project Step 4 Draft Version
-- File: data-manipulation-queries.sql
-- Description: This file contains SELECT, INSERT, UPDATE and
--   DELETE queries to let users interact with data.

-- The ‘:’ preceding a variable will be used to denote 
-- user-entered input

-- Note: This file is not yet complete.

-- CREATE
INSERT INTO `customers` (fname, lname, email, password, phone_number)
VALUES (:fnameInput, :lnameInput, :emailInput, :passwordInput, :phone_numberInput);

INSERT INTO `carts` (customer_id, cart_name) VALUES (:customer_id, :cart_name);

INSERT INTO `orders` (customer_id, billing_street, billing_city, billing_state, billing_zip, shipping_street, shipping_city, shipping_state, shipping_zip, shipped, pickup_or_ship, has_paid, delivered, order_date)
VALUES (:customer_id, :billing_street, :billing_city, :billing_state, :billing_zip, :shipping_street, :shipping_city, :shipping_state, :shipping_zip, :shipped, :pickup_or_ship, :has_paid, :delivered, :order_date);

INSERT INTO `products` (product_name, category, vendor, price, image, quantity_available)
VALUES (:product_name, :category, :vendor, :price, :image, :quantity_available);

INSERT INTO `products_carts` (cart_id, product_id, product_quantity)
VALUES (:cart_id, :product_id, :product_quantity);

INSERT INTO `products_orders` (order_id, product_id, product_quantity)
VALUES (:order_id, :product_id, :product_quantity);

-- READ
SELECT product_name, price, image FROM products WHERE category = :category;

SELECT customer_id
FROM customers
WHERE :emailInput IN

--    READ cart (Requires a join)
SELECT carts.cart_name AS cart_name, products.product_name AS product_name, products.price AS price, cart_item.product_quantity AS quantity 
FROM (SELECT cart_id, customer_id, cart_name FROM carts WHERE customer_id = :customer_id) AS carts 
INNER JOIN products_carts AS cart_item ON carts.cart_id = cart_item.cart_id 
INNER JOIN products ON products.product_id = cart_item.product_id;

-- UPDATE
UPDATE `customers` 
SET fname=:fname, lname=:lname, email=:email, password=:password, phone_number=:phone_number
WHERE id=:id;

UPDATE `carts`
SET customer_id=:customer_id, cart_name=:cart_name
WHERE cart_id=:cart_id;

UPDATE `orders`
SET customer_id=:customer_id, billing_street=:billing_street, billing_city=:billing_city, billing_state=:billing_state, 
billing_zip=:billing_zip, shipping_street=:shipping_street, shipping_city=:shipping_city, shipping_state=:shipping_state, 
shipping_zip=:shipping_zip, shipped=:shipped, pickup_or_ship=:pickup_or_ship, has_paid=:has_paid, delivered=:delivered, order_date=:order_date
WHERE order_id=:order_id;

UPDATE `products`
SET product_name=:product_name, category=:category, vendor=:vendor, price=:price, image=:image, quantity_available=:quantity_available
WHERE product_id=:product_id;

UPDATE `products_carts`
SET product_quantity=:product_quantity
WHERE cart_id=:cart_id AND product_id=:product_id;

UPDATE `products_orders`
SET product_quantity=:product_quantity
WHERE order_id=:order_id AND product_id=:product_id;

-- DELETE
DELETE FROM `customers` WHERE user_id=:id;

DELETE FROM `carts` WHERE cart_id=:cart_id