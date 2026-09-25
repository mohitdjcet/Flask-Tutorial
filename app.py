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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
