-- Name: Joshua Kaiser, Timothy Yoon
-- Group: 57
-- Assignment: Project Step 6
-- File: data-manipulation-queries.sql
-- Description: This file contains SELECT, INSERT, UPDATE and
--   DELETE queries to let users interact with data.

-- The ‘:’ preceding a variable will be used to denote 
-- user-entered input

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
SELECT customer_id, fname, lname, email, phone_number 
FROM `customers`;

    --    READ cart (Requires a join)
SELECT carts.cart_name AS cart_name, products.product_name AS product_name, products.price AS price, cart_item.product_quantity AS quantity 
FROM (SELECT cart_id, customer_id, cart_name FROM `carts` WHERE customer_id = :customer_id) AS carts 
INNER JOIN `products_carts` AS cart_item ON carts.cart_id = cart_item.cart_id 
INNER JOIN `products` ON products.product_id = cart_item.product_id;

SELECT customer_id, billing_street, billing_city, billing_state, billing_zip, shipping_street, shipping_city, shipping_state, shipping_zip, shipped, pickup_or_ship, has_paid, delivered, order_date
FROM `orders`
WHERE order_id=:order_id;


SELECT product_name, category, vendor, price, image, quantity_available 
FROM `products` WHERE category = :category;

SELECT orders.billing_street, orders.billing_city, orders.billing_state, orders.billing_zip, orders.shipping_street, orders.shipping_city, orders.shipping_state, orders.shipping_zip, orders.shipped, orders.pickup_or_ship, orders.has_paid, orders.delivered, orders.order_date, order_item.product_quantity, products.product_name, products.category, products.vendor, products.price, products.image, products.quantity_available 
FROM (SELECT * FROM `orders` WHERE orders.order_id=:order_id) AS orders
INNER JOIN `products_orders` AS order_item ON orders.order_id=order_item.order_id
INNER JOIN `products` ON products.product_id=order_item.product_id;
-- OR --
SELECT orders.billing_street, orders.billing_city, orders.billing_state, orders.billing_zip, orders.shipping_street, orders.shipping_city, orders.shipping_state, orders.shipping_zip, orders.shipped, orders.pickup_or_ship, orders.has_paid, orders.delivered, orders.order_date, order_item.product_quantity, products.product_name, products.category, products.vendor, products.price, products.image, products.quantity_available 
FROM `orders`
INNER JOIN `products_orders` AS order_item ON orders.order_id=order_item.order_id
INNER JOIN `products` ON products.product_id=order_item.product_id
WHERE orders.order_id=:order_id;

-- UPDATE
UPDATE `customers` 
SET fname=:fname, lname=:lname, email=:email, password=:password, phone_number=:phone_number
WHERE customer_id=:customer_id;

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
DELETE FROM `customers`
WHERE customer_id=:id;

DELETE FROM `carts`
WHERE cart_id=:cart_id;

DELETE FROM `orders`
WHERE order_id = :order_id;

DELETE FROM `products`
WHERE product_id = :product_id;

DELETE FROM `products_carts`
WHERE cart_id = :cart_id AND product_id = :product_id;

DELETE FROM `products_orders`
WHERE order_id = :order_id AND product_id = :product_id;
