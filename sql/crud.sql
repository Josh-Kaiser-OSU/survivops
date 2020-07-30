
-- Name: Joshua Kaiser, Timothy Yoon
-- Group: 57
-- Assignment: Project Step 4 Draft Version
-- File: crud.sql
-- Description: This file contains SELECT, INSERT, UPDATE and
--   DELETE queries to let users interact with data.

-- The ‘:’ preceding a variable will be used to denote 
-- user-entered input

-- Note: This file is not yet complete.

-- signin.html
--    CREATE
-- Add a new customer if the user signs up
INSERT INTO `customers` (fname, lname, email, password, phone_number)
VALUES (:fnameInput, :lnameInput, :emailInput, :passwordInput, :phone_numberInput);

--    READ
-- Select an existing customer if the user signs in
SELECT customer_id
FROM customers
WHERE :emailInput IN

--    UPDATE

--    DELETE

-- index.html
--    CREATE (Creating products happens on the admin page)

--    READ
SELECT (product_name, price, image) FROM products WHERE category = :category;
--    UPDATE
UPDATE 
--    DELETE (Deleting products happens on the admin page)

-- product.html
--    CREATE (Creating products happens on the admin page)

--    READ

--    UPDATE

--    DELETE (Deleting products happens on the admin page)

-- cart.html
--    CREATE
INSERT INTO carts (customer_id, cart_name) VALUES (:customer_id, :cart_name);
--    READ (Requires a join)
SELECT carts.cart_name, products_carts.product_quantity, products.product_name, products.category, products.vendor, products.price, products.image, products.quantity_available FROM carts
INNER JOIN products_carts ON cart_id
INNER JOIN products ON product_id
WHERE carts.customer_id=:customer_id;

--    UPDATE


--    DELETE

-- order.html
--    CREATE

--    READ

--    UPDATE

--    DELETE

-- contact.html (No CRUD functionality is used in the contact -- page)

-- account.html
--    CREATE (Creating accounts is done on the signup page)

--    READ
SELECT fname, lname, email, password, phone_number FROM customers WHERE customer_id = :customer_id;
--    UPDATE
UPDATE customers SET email=’new-email’, password=’new-password’ WHERE user_id = :id;
--    DELETE
DELETE FROM customers WHERE user_id = :id;

-- admin.html
--    CREATE

--    READ

--    UPDATE

--    DELETE
