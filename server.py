from flask import Flask, render_template

app = Flask(__name__)

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

if __name__ == "__main__":
    app.run(debug=True)
