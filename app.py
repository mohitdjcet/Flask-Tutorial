from flask import Flask,request,jsonify,session
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY","dev-only-change-this")

client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")
print("MD connected Successfully !")
db = client['flask_db']
users_collection = db["users"]

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "user_id" not in session:
            return jsonify({
                "message":"Please login First"
            }),401
        return f(*args,**kwargs)
    return decorated_function

@app.route("/")
def home():
    return "Flask is working !"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "message":"Valid JSON object is required"
        }),400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all(
        isinstance(value,str) and value.strip()
        for value in [name,email,password]
    ):
        return jsonify({
            "message":"Name, email and password are required"
        }),400

    name = name.strip()
    email = email.strip().lower()

    if "@" not in email or "." not in email.rsplit("@",1)[-1]:
        return jsonify({
            "message":"Invalid email address"
        }),400

    if len(password)<8:
        return jsonify({
            "message":"Password must be at least 8 Char"
        }),400

    existing_user = users_collection.find_one({
        "email":email
    }) 
    if existing_user:
        return jsonify({
            "message":"Email already registered"
        })

    hashed_password = generate_password_hash(password)

    result = users_collection.insert_one({
        "name":name,
        "email":email,
        "password":hashed_password
    })

    return jsonify({
        "message":"User Registration successfully !",
        "user_id":str(result.inserted_id),
        "name":name,
        "email":email
    }),201

@app.route("/login", methods=["POST"])
def login():
    data= request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "message": "Valid JSON object is required"
        }), 400
    email = data.get("email", "").strip().lower()
    password= data.get("password","")

    if not email or not password:
        return jsonify({
            "message":"Email and password are required !"
        }),400
    user = users_collection.find_one({
        "email":email
    })
    if not user or not check_password_hash(
        user.get("password",""),
        password
    ):
        return jsonify({
            "message":"Invalid Email or password"
        }),401

    session.clear()
    session["user_id"]=str(user["_id"])
    session["user_name"]= user.get("name","")
    return jsonify({
        "message":"Login Successfully !",
        "user":{
            "id":str(user["_id"]),
            "name": user.get("name",""),
            "email": user["email"]
        }
    }),200

@app.route("/profile",methods=["GET"])
@login_required
def profile():
    return jsonify({
        "message":"Profile fetched successfully !",
        "user":{
            "id": session["user_id"],
            "name":session.get("user_name","")
        }
    }),200

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return jsonify({
        "message":"Logout successfully !"
    }),200

if __name__ == "__main__":
    app.run(debug=True)
