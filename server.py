from flask import Flask, render_template, request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # Get all products from db
        db_connection = connect_to_database()
        query = "SELECT product_id, product_name, category, vendor, price\
        , image, quantity_available FROM `products`;"
        result = execute_query(db_connection, query).fetchall()
        
        # Get all the categories from db
        query = "SELECT category FROM `products`;"
        category_result = execute_query(db_connection, query).fetchall()
        categories = set()
        for r in category_result:
            categories.add(r[0])

        # Render the page
        return render_template("index.html", rows=result, categories=categories, filters=['',''])

    elif request.method == 'POST':
        # Get all the filters from the form
        try:
            category = request.form['category']
        except KeyError:
            category = ''
        min_price = request.form['min-price']
        max_price = request.form['max-price']

        # Build the query from the user-entered filters and query db
        db_connection = connect_to_database()
        constraints = "WHERE 1"
        if min_price != "":
            constraints += " and price > " + str(min_price)
        if max_price != "":
            constraints += " and price < " + str(max_price)
        if category != "":
            constraints += ' and category="' + str(category) + '"'
        query = "SELECT product_id, product_name, category, vendor, price, image, \
        quantity_available FROM `products`" + constraints + ";"
        result = execute_query(db_connection, query).fetchall()

        # Get all the categories
        query = "SELECT category FROM `products`;"
        category_result = execute_query(db_connection, query).fetchall()
        categories = set()
        for r in category_result:
            categories.add(r[0])
        
        # Render the page with the filtered data.
        return render_template("index.html", rows=result, categories=categories, filters=[min_price, max_price])


@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    '''Allow the user to sign in or register as a new customer.'''
    # Handle customer registration
    if request.method == 'POST':
        db_connection = connect_to_database()

        # Gather all user data
        fname = request.form['sign-up-fname-field']
        lname = request.form['sign-up-lname-field']
        email = request.form['sign-up-email-field']
        password = request.form['sign-up-password-field']
        phone = request.form['sign-up-phone-number-field']

        # Create and execute query to add a new customer to the database
        query = 'INSERT INTO `customers` (fname, lname, email, password, phone_number) \
                 VALUES (%s, %s, %s, %s, %s);'
        customer_data = (fname, lname, email, password, phone)
        execute_query(db_connection, query, customer_data)

        # Redirect the user to the home page after registering
        return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template("signin.html")


@app.route('/product/')
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id = 1):
    '''View a product and add a selected quantity to a selected cart.'''
    db_connection = connect_to_database()
    if request.method == 'GET':
        # Get all info for the product with the given product_id
        product_query = 'SELECT * FROM `products` WHERE product_id = %s;' % (product_id)
        product_result = execute_query(db_connection, product_query).fetchone()
        if product_result == None:
            return "A product with id " + str(product_id) + " cannot be found."

        # Get all carts from the database
        carts_query = 'SELECT * FROM `carts`;'
        carts_result = execute_query(db_connection, carts_query).fetchall()
        return render_template("product.html", product=product_result, carts=carts_result)

    elif request.method == 'POST':
        # Calculate the quantity of product remaining after the customer adds to the cart
        product_qty_query = 'SELECT quantity_available FROM `products` WHERE product_id = %s;' % (product_id)
        product_qty_result = execute_query(db_connection, product_qty_query).fetchone()[0]
        qty_to_order = int(request.form['quantity-to-order'])
        qty_remaining = product_qty_result - qty_to_order
        cart_id = int(request.form['carts'])

        # Update the quantity_available attribute of the product
        update_qty_avail_query = 'UPDATE products \
                                  SET quantity_available = %s \
                                  WHERE product_id = %s;' % (qty_remaining, product_id)
        update_qty_avail_result = execute_query(db_connection, update_qty_avail_query).fetchall()

        # Add the product to the cart
        add_prod_to_cart_query = 'REPLACE INTO products_carts (cart_id, product_id, product_quantity) \
                                  VALUES (%s, %s, %s);' % (cart_id, product_id, qty_to_order)
        add_prod_to_cart_result = execute_query(db_connection, add_prod_to_cart_query).fetchall()

        # Get the customer ID associated with the selected cart
        get_cust_id_query = 'SELECT customer_id FROM `carts` WHERE cart_id = %s;' % (cart_id)
        get_cust_id_result = execute_query(db_connection, get_cust_id_query).fetchone()[0]
        if get_cust_id_result == None:
            get_cust_id_result = 0
        return redirect(url_for('cart') + str(get_cust_id_result))


@app.route('/cart/')
@app.route('/cart/<int:customer_id>/', methods=['GET', 'POST'])
@app.route('/cart/<int:customer_id>/<int:cart_id>', methods=['GET', 'POST'])
def cart(customer_id=0, cart_id=0):
    db_connection = connect_to_database()
    if customer_id == 0:
        customer = "customer_id IS NULL"
    else:
        customer = "customer_id=" + str(customer_id)

    if request.method == 'GET':
        # Get all carts associated with the customer
        query = "SELECT cart_name, cart_id FROM `carts` WHERE " + customer + ';'
        cart_result = execute_query(db_connection, query).fetchall()
        carts = []
        for item in cart_result:
            carts.append([item[0], item[1]])

        # If the cart_id is not specified by the user, the first cart in the cart list will be displayed
        if cart_id == 0 and carts:
            cart_id = carts[0][1]

        # Get all items in the specified cart
        query = ''.join(["SELECT products.product_id, carts.cart_id, \
        carts.cart_name AS cart_name, products.product_name AS product_name, ",
        "products.price AS price, cart_item.product_quantity AS quantity ",
        "FROM (SELECT cart_id, customer_id, cart_name FROM `carts` WHERE ",
        customer,
        ") AS carts INNER JOIN `products_carts` AS cart_item ON carts.cart_id = \
        cart_item.cart_id ",
        "INNER JOIN `products` ON products.product_id = cart_item.product_id ",
        "WHERE carts.cart_id=" + str(cart_id) + ";"])
        result = execute_query(db_connection, query).fetchall()

        # Render the page
        return render_template("cart.html", carts=carts, cart_id=cart_id, cartitems=result, customer_id=customer_id)

    elif request.method == 'POST':
        # Get form data
        cmd = request.form['cmd']
        cart_id = request.form['cart_id']
        product_id = request.form['product_id']
        qty = request.form['quantity']

        if cmd == "Update":
            # Updates the quantity of a particular product in the cart
            query = "UPDATE `products_carts` SET product_quantity=\
            " + str(qty) + " WHERE cart_id=" + str(cart_id) + " AND \
            product_id=" + str(product_id) + ";"
            result = execute_query(db_connection, query).fetchall()
        elif cmd == "Remove":
            # Delete product from cart
            query = "DELETE FROM `products_carts` WHERE cart_id = \
            " + str(cart_id) + " AND product_id = " + str(product_id) + ";"
            result = execute_query(db_connection, query).fetchall()
        elif cmd == "new_cart":
            # Create a new cart with a user-defined name
            cart_name = request.form['new_cart_name']
            if customer_id == 0:
                customer = "NULL"
            else:
                customer = customer_id
            query = "INSERT INTO `carts` (customer_id, cart_name) VALUES (\
            " + str(customer) + ', "' + str(cart_name) + '");'
            result = execute_query(db_connection, query).fetchall()
        elif cmd == "make_public":
            # Make a cart public by setting customer_id = Null
            query = "UPDATE `carts` SET customer_id=NULL WHERE cart_id=" + str(cart_id) + ";"
            result = execute_query(db_connection, query).fetchall()
        elif cmd == "delete_cart":
            # Delete a cart (cascades to delete the products in products_carts too)
            query = "DELETE FROM `carts` WHERE cart_id=" + str(cart_id) + ";"
            result = execute_query(db_connection, query).fetchall()
        return redirect('cart/' + str(customer_id))


@app.route('/order/', methods=['GET', 'POST'])
@app.route('/order/<int:cart_id>', methods=['GET', 'POST'])
def order(cart_id = 1):
    '''Allow a customer to place an order.'''
    db_connection = connect_to_database()
    # Display all cart items in the "Review items" section of the page
    if request.method == 'GET':
        # Get all rows from the products_carts table with the given cart_id
        prod_in_cart_query = 'SELECT P.image, P.product_name, P.vendor, P.price, PC.product_quantity \
                              FROM `products_carts` PC \
                              INNER JOIN `products` P ON PC.product_id = P.product_id \
                              WHERE cart_id = %s;' % (cart_id)
        prod_in_cart_result = execute_query(db_connection, prod_in_cart_query).fetchall()

        # Render the order template only if there are products in the cart; otherwise show an error message
        if prod_in_cart_result:
            return render_template('order.html', cart_products=prod_in_cart_result, cart_id=cart_id)
        else:
            return "The cart with id " + str(cart_id) + " has no products."

    # Add a new entry to the orders and products_orders tables
    if request.method == 'POST':
        # Get the customer's ID
        get_cust_id_query = 'SELECT CU.customer_id \
                             FROM `customers` CU \
                             INNER JOIN `carts` CA ON CA.customer_id = CU.customer_id \
                             WHERE cart_id = %s;' % (cart_id)
        get_cust_id_result = execute_query(db_connection, get_cust_id_query).fetchone()
        cust_id = get_cust_id_result

        # Get all the data from the form
        billing_street = str(request.form['billing-street'])
        billing_city = str(request.form['billing-city'])
        billing_state = str(request.form['billing-state'])
        billing_zip = str(request.form['billing-zip'])
        shipping_street = str(request.form['shipping-street'])
        shipping_city = str(request.form['shipping-city'])
        shipping_state = str(request.form['shipping-state'])
        shipping_zip = str(request.form['shipping-zip'])
        shipped = False
        delivery_option = str(request.form['delivery-option'])
        if delivery_option == 'pick-up':
            pickup_or_ship = True
        else:
            pickup_or_ship = False
        has_paid = True
        delivered = False
        # Get the current date and time, courtesy of https://www.programiz.com/python-programming/datetime/current-datetime
        order_date = str(datetime.now())[:19]
        # Insert a new row into the orders table
        create_order_query = 'INSERT INTO `orders`(customer_id, billing_street, billing_city, billing_state, billing_zip, shipping_street, shipping_city, shipping_state, shipping_zip, shipped, pickup_or_ship, has_paid, delivered, order_date) \
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        order_data = (cust_id, billing_street, billing_city, billing_state, billing_zip, shipping_street, shipping_city, shipping_state, shipping_zip, shipped, pickup_or_ship, has_paid, delivered, order_date)
        execute_query(db_connection, create_order_query, order_data)

        # Gather data to insert into the products_orders table
        # Get the last order_id from the orders table, courtesy of https://www.tutorialspoint.com/get-last-entry-in-a-mysql-table
        get_last_order_id_query = 'SELECT order_id FROM `orders` ORDER BY order_id DESC LIMIT 1;'
        get_last_order_id_result = execute_query(db_connection, get_last_order_id_query).fetchone()[0]
        order_id = get_last_order_id_result

        # Get all product_id and product_quantity values from the products_carts table
        get_prod_id_qty_query = 'SELECT PC.product_id, PC.product_quantity \
                                 FROM `products_carts` PC \
                                 INNER JOIN `carts` C ON C.cart_id = PC.cart_id \
                                 WHERE C.cart_id = %s;' % (cart_id)
        get_prod_id_qty_result = execute_query(db_connection, get_prod_id_qty_query).fetchall()

        # Use each (product_id, product_quantity) tuple in adding a new row to the products_orders table
        for tup in get_prod_id_qty_result:
            insert_products_orders_query = 'INSERT INTO `products_orders`(order_id, product_id, product_quantity) \
                                            VALUES (%s, %s, %s);'
            products_orders_data = (order_id, tup[0], tup[1])
            execute_query(db_connection, insert_products_orders_query, products_orders_data)

        return redirect(url_for('home'))  # Redirect user to the home page


@app.route("/account/")
@app.route("/account/<int:customer_id>", methods=['GET', 'POST'])
def account(customer_id=0):
    db_connection = connect_to_database()
    if request.method == 'GET':
        # Get all customer ids to check if user-entered cutomer_id is valid
        query = "SELECT customer_id FROM `customers`;"
        customer_id_result = execute_query(db_connection, query).fetchall()
        id_set = set()
        for num in customer_id_result:
            id_set.add(num[0])
        if customer_id not in id_set:
            return render_template("account.html", info=[], orders=[])

        # Get customer info from db
        query = ''.join(["SELECT customer_id, fname, lname, email, password, phone_number ",
        "FROM `customers` WHERE customer_id=",
        str(customer_id), ";"])
        result = execute_query(db_connection, query).fetchall()

        # Get order info for the customer from db
        query = ''.join([
            "SELECT order_id, billing_street, billing_city, billing_state, billing_zip, ",
            "shipping_street, shipping_city, shipping_state, shipping_zip, shipped, ",
            "pickup_or_ship, has_paid, delivered, order_date FROM `orders` WHERE customer_id=",
            str(customer_id), ";"
        ])
        orders = execute_query(db_connection, query).fetchall()
        
        # Get items for every order from db
        order_items = []
        for order in orders:
            query = "SELECT products.product_name, order_item.product_quantity \
            FROM (SELECT order_id FROM `orders` WHERE orders.order_id=" + str(order[0]) + ") AS orders \
            INNER JOIN `products_orders` AS order_item ON orders.order_id=order_item.order_id \
            INNER JOIN `products` ON products.product_id=order_item.product_id;"

            order_items_result = execute_query(db_connection, query).fetchall()
            order_items_list = []
            for item in order_items_result:
                order_items_list.append(list(item))
            order_items.append([order[0], order_items_list])
        return render_template("account.html", info=result, orders=orders, order_items=order_items)
    
    elif request.method == 'POST':
        # Update account info
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone_number']
        query = ''.join(["UPDATE `customers` SET email=" , '"' + str(email) + '"' + ", password=" + '"', str(password),
        '"' + ", phone_number=" + '"' + str(phone_number)+ '"' + " WHERE customer_id=" + str(customer_id) + ";"])
        result = execute_query(db_connection, query).fetchall()
        return redirect('/account/' + str(customer_id))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin/")
def admin():
    '''
    Allow administrators to view all a list of all customers and a list of orders by customer ID.
    Admins can also add, update or delete products from the database.
    '''
    db_connection = connect_to_database()
    # Fill out the "Customer List" section on the page
    # Get all customers from the database
    get_all_cust_query = 'SELECT * FROM `customers`;'
    get_all_cust_result = execute_query(db_connection, get_all_cust_query).fetchall()

    # Get all products from the database
    get_all_prod_query = 'SELECT * FROM `products`;'
    get_all_prod_result = execute_query(db_connection, get_all_prod_query).fetchall()

    # Pass the customers and products into the admin.html template to be displayed
    return render_template("admin.html", customers=get_all_cust_result, products=get_all_prod_result)


@app.route("/admin/show-orders/", methods=['GET', 'POST'])
def admin_show_orders():
    '''List a customer's orders based on the customer ID submitted on the admin page.'''
    db_connection = connect_to_database()

    # Get all orders for the given customer_id
    cust_id = str(request.form['customer-id'])
    get_all_ord_query = 'SELECT * FROM `orders` WHERE customer_id = %s;' % (cust_id)
    get_all_ord_result = execute_query(db_connection, get_all_ord_query).fetchall()

    # Pass the orders to the template to be displayed
    return render_template("admin-show-orders.html", orders=get_all_ord_result)


@app.route("/admin/add-product/", methods=['GET', 'POST'])
def admin_add_product():
    '''Add a new product to the database from the admin page.'''
    db_connection = connect_to_database()

    # Add a product to the products table
    if request.method == 'POST':
        for item in request:
            print(item)
        # Get data from the form
        product_name = request.form['new-product-name']
        category = request.form['new-category']
        vendor = request.form['new-vendor']
        price = request.form['new-price']
        qty_available = request.form['new-qty-available']
        image = request.form['new-image']
        
        # Create and execute query to insert a new row into the products table
        add_new_prod_query = 'REPLACE INTO `products` (product_name, category, vendor, price, quantity_available, image) \
                              VALUES (%s, %s, %s, %s, %s, %s);'
        prod_data = (product_name, category, vendor, price, qty_available, image)  # Gather form data
        execute_query(db_connection, add_new_prod_query, prod_data)

        return redirect(url_for('admin'))  # Redirect user back to the admin page


@app.route('/admin/update-product/<int:product_id>/', methods=['GET', 'POST'])
def admin_update_product(product_id):
    '''Update a product that exists in the database.'''
    db_connection = connect_to_database()

    # Get the existing product info and pass it into a template
    if request.method == 'GET':
        # Create and execute query to get all product info
        get_prod_info_query = 'SELECT * FROM `products` WHERE product_id = %s;' % (product_id)
        get_prod_info_result = execute_query(db_connection, get_prod_info_query).fetchone()
        return render_template('admin-update-product.html', product=get_prod_info_result)

    # Update the product using the submitted form
    if request.method == 'POST':
        # Gather form data
        product_name = request.form['product-name']
        category = request.form['category']
        vendor = request.form['vendor']
        price = request.form['price']
        qty_available = request.form['qty-available']
        image = request.form['image']

        # Create and execute query to update the product
        update_prod_query = 'UPDATE `products` SET product_name = %s, category = %s, vendor = %s, price = %s, image = %s, quantity_available = %s \
                             WHERE product_id = %s;'
        data = (product_name, category, vendor, price, image, qty_available, product_id)
        update_prod_result = execute_query(db_connection, update_prod_query, data)

        return redirect(url_for('admin'))  # Redirect user back to the admin page


@app.route('/admin/delete-product/<int:product_id>/', methods=['GET', 'POST'])
def admin_delete_product(product_id):
    '''Delete the specified row from the products table.'''
    db_connection = connect_to_database()
    if request.method == 'POST':
        # Create and execute a query to delete the product
        del_prod_query = 'DELETE FROM `products` WHERE product_id = %s;'
        data = (product_id,)
        del_prod_result = execute_query(db_connection, del_prod_query, data)

        return redirect(url_for('admin'))  # Redirect user back to the admin page


if __name__ == "__main__":
    app.run(debug=True)
