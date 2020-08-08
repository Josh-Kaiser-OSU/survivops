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

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/cart")
def cart():
    print("Fetching and rendering products web page")
    db_connection = connect_to_database()
    # Will get customer_id based on user input later
    customer_id = 2
    query = ''.join(["SELECT carts.cart_name AS cart_name, products.product_name AS product_name, ",
    "products.price AS price, cart_item.product_quantity AS quantity ",
    "FROM (SELECT cart_id, customer_id, cart_name FROM `carts` WHERE customer_id = ",
    str(customer_id),
    ") AS carts INNER JOIN `products_carts` AS cart_item ON carts.cart_id = cart_item.cart_id ",
    "INNER JOIN `products` ON products.product_id = cart_item.product_id;"])
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template("cart.html", cartitems=result)

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/account")
def account():
    # Will get customer_id based on user input later
    customer_id = 1
    db_connection = connect_to_database()
    query = ''.join(["SELECT customer_id, fname, lname, email, password, phone_number ",
    "FROM `customers` WHERE customer_id=",
    str(customer_id), ";"])
    result = execute_query(db_connection, query).fetchall()
    print(result)
    query = ''.join(["SELECT carts.cart_name AS cart_name, products.product_name AS product_name, ",
    "products.price AS price, cart_item.product_quantity AS quantity ",
    "FROM (SELECT cart_id, customer_id, cart_name FROM `carts` WHERE customer_id = ",
    str(customer_id),
    ") AS carts INNER JOIN `products_carts` AS cart_item ON carts.cart_id = cart_item.cart_id ",
    "INNER JOIN `products` ON products.product_id = cart_item.product_id;"])
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
