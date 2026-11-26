import os
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///shop.db")
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

with app.app_context():
    db.create_all()
    if Product.query.count() == 0:
        db.session.add_all([
            Product(name="Garri (5 lb)", price=12.99, stock=50),
            Product(name="Egusi (1 lb)", price=9.99, stock=40),
            Product(name="Palm Oil (1 L)", price=8.49, stock=30),
            Product(name="Ground Crayfish", price=7.99, stock=25),
            Product(name="Indomie (carton of 40)", price=24.99, stock=20),
        ])
        db.session.commit()

@app.route("/")
def home():
    rows = "".join(
        f"<li>{p.name} - ${p.price} ({p.stock} left) "
        f"<a href='/buy/{p.id}'>Buy</a></li>"
        for p in Product.query.all()
    )
    return f"<h1>Mama Ngozi's Pantry</h1><ul>{rows}</ul>"

@app.route("/buy/<int:pid>")
def buy(pid):
    p = db.session.get(Product, pid)
    if p and p.stock > 0:
        p.stock -= 1
        db.session.commit()
    return redirect("/")

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)