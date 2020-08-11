from flask import Flask, render_template, request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        print("Fetching and rendering products web page")
        db_connection = connect_to_database()
        query = "SELECT product_name, category, vendor, price, image, quantity_available FROM `products`;"
        result = execute_query(db_connection, query).fetchall()
        categories = set()
        for r in result:
            categories.add(r[1])
        categories = list(categories)
        print(categories)
        return render_template("index.html", rows=result, categories=categories)
    elif request.method == 'POST':
        try:
            category = request.form['category']
        except KeyError:
            category = ''
        min_price = request.form['min-price']
        max_price = request.form['max-price']
        print(category, min_price, max_price)
        db_connection = connect_to_database()
        constraints = "WHERE 1"
        if min_price != "":
            constraints += " and price > " + str(min_price)
        if max_price != "":
            constraints += " and price < " + str(max_price)
        if category != "":
            constraints += ' and category="' + str(category) + '"'
        query = "SELECT product_name, category, vendor, price, image, quantity_available FROM `products`" + constraints + ";"
        result = execute_query(db_connection, query).fetchall()
        categories = set()
        for r in result:
            categories.add(r[1])
        categories = list(categories)
        print(categories)
        return render_template("index.html", rows=result, categories=categories)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        db_connection = connect_to_database()

        # Gather all customer data
        fname = request.form['sign-up-fname-field']
        lname = request.form['sign-up-lname-field']
        email = request.form['sign-up-email-field']
        password = request.form['sign-up-password-field']
        phone = request.form['sign-up-phone-number-field']

        query = 'INSERT INTO `customers` (fname, lname, email, password, phone_number) \
                 VALUES (%s, %s, %s, %s, %s);'
        customer_data = (fname, lname, email, password, phone)
        execute_query(db_connection, query, customer_data)

        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template("signin.html")

@app.route('/product/')
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id = 1):
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
        return redirect(url_for('cart') + str(get_cust_id_result))

@app.route('/cart/')
@app.route('/cart/<int:customer_id>', methods=['GET', 'POST'])
def cart(customer_id=1):
    db_connection = connect_to_database()
    if request.method == 'GET':
        print("Fetching and rendering cart web page")
        # Will get customer_id based on user input later
        query = ''.join(["SELECT products.product_id, carts.cart_id, carts.cart_name AS cart_name, products.product_name AS product_name, ",
        "products.price AS price, cart_item.product_quantity AS quantity ",
        "FROM (SELECT cart_id, customer_id, cart_name FROM `carts` WHERE customer_id = ",
        str(customer_id),
        ") AS carts INNER JOIN `products_carts` AS cart_item ON carts.cart_id = cart_item.cart_id ",
        "INNER JOIN `products` ON products.product_id = cart_item.product_id;"])
        result = execute_query(db_connection, query).fetchall()
        carts = set()
        for item in result:
            carts.add(item[2])
        return render_template("cart.html", carts=carts, cartitems=result)
    elif request.method == 'POST':
        cmd = request.form['cmd']
        qty = request.form['quantity']
        cart_id = request.form['cart_id']
        product_id = request.form['product_id']

        query = "SELECT customer_id FROM `carts` WHERE cart_id=" + str(cart_id)
        result = execute_query(db_connection, query).fetchall()
        customer_id = result[0][0]
        if cmd == "Remove":
            # Delete product from cart
            query = "DELETE FROM `products_carts` WHERE cart_id = " + str(cart_id) + " AND product_id = " + str(product_id) + ";"
            result = execute_query(db_connection, query).fetchall()
        else:
            # Update product in cart
            query = "UPDATE `products_carts` SET product_quantity=" + str(qty) + " WHERE cart_id=" + str(cart_id) + " AND product_id=" + str(product_id) + ";"
            result = execute_query(db_connection, query).fetchall()
        return redirect('cart/' + str(customer_id))
        

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/account")
def account():
    # Will get customer_id based on user input later
    customer_id = 2
    db_connection = connect_to_database()
    query = ''.join(["SELECT customer_id, fname, lname, email, password, phone_number ",
    "FROM `customers` WHERE customer_id=",
    str(customer_id), ";"])
    result = execute_query(db_connection, query).fetchall()
    print(result)
    query = ''.join([
        "SELECT order_id, billing_street, billing_city, billing_state, billing_zip, ",
        "shipping_street, shipping_city, shipping_state, shipping_zip, shipped, ",
        "pickup_or_ship, has_paid, delivered, order_date FROM `orders` WHERE customer_id=",
        str(customer_id), ";"
    ])
    orders = execute_query(db_connection, query).fetchall()
    print(orders)
    return render_template("account.html", info=result, orders=orders)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
