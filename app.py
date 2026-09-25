from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

app = Flask(__name__)

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_URL

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True
    )
    name = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        db.String(120),
        nullable=False
    )
    age = db.Column(
        db.Integer
    )
    orders = db.relationship(
        "Order",
        backref = "user",
        lazy = True
    )

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(
        db.Integer,
        primary_key = True
    )   
    product = db.Column(
        db.String(100),
        nullable=False
    )
    amount = db.Column(
        db.Float,
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

@app.route("/")
def home():
    return "Flask + MySQL is working !"

@app.route("/users",methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    user = User(
        name=name,
        email=email,
        age=age
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message":"User Created Successfully !",
        "user_id":user.id
    }),201

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    product = data.get("product")
    amount = data.get("amount")
    user_id = data.get("user_id")

    order = Order(
        product=product,
        amount=amount,

        user_id=user_id
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({
        "message":"Order Created Successfully !",
        "order_id":order.id
    }),201

@app.route("/users/<int:user_id>/orders", methods=["GET"])
def get_user_orders(user_id):
    user = db.get_or_404(User,user_id)
    orders = user.orders
    orders_data = []
    for order in orders:
        orders_data.append({
            "id":order.id,
            "product":order.product,
            "amount":order.amount
        })
    return jsonify({
        "user":user.name,
        "orders":orders_data
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
