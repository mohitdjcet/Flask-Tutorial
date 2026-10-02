from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")

print("MD connected Successfully !")

db = client['flask_db']
users_collection = db["users"]

@app.route("/")
def home():
    return "Flask is working !"

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    results = users_collection.insert_one(data)
    return jsonify({
        "message":"User Created Successfully !",
        "id": str(results.inserted_id)
    }),201

@app.route("/users/bulk", methods=["POST"])
def create_user_bulk():
    data = request.get_json()
    result = users_collection.insert_many(data)
    ids = [str(user_id) for user_id in result.inserted_ids]
    return jsonify({
        "message":"User Created Successfully !",
        "id": ids
    }),201

@app.route("/users", methods=["GET"])
def get_users():
    users = users_collection.find()
    users_data= []
    for user in users:
        users_data.append({
            "id":str(user["_id"]),
            "name":user["name"],
            "email":user["email"],
            "age":user["age"]
        })
    return jsonify(users_data)

@app.route("/users/first", methods=["GET"])
def get_first_users():
    user = users_collection.find_one()

    if user is None:
        return jsonify({
            "message":"User not found"
        }),404
    
    return jsonify({
        "id":str(user["_id"]),
        "name":user["name"],
        "email":user["email"],
        "age":user["age"]
    })

@app.route("/users/<user_id>", methods=["GET"])
def get_id_users(user_id):
    user = users_collection.find_one({
        "_id":ObjectId(user_id)
    })

    if user is None:
        return jsonify({
            "message":"User not found"
        }),404
    
    return jsonify({
        "id":str(user["_id"]),
        "name":user["name"],
        "email":user["email"],
        "age":user["age"]
    })

if __name__ == "__main__":
    app.run(debug=True)
