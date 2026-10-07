from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")
print("MD connected Successfully !")
db = client['flask_db']
users_collection = db["users"]

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
            "mesage":"Invalid email address"
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

if __name__ == "__main__":
    app.run(debug=True)
