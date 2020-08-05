from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

@app.route("/")
def home():
    print("Fetching and rendering products web page")
    db_connection = connect_to_database()
    query = "SELECT product_name, category, vendor, price, image, quantity_available FROM `products`;"
    result = execute_query(db_connection, query).fetchall()
    categories = []
    for r in result:
        categories.append(r[1])
    print(categories)
    return render_template("index.html", rows=result, categories=categories)

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
