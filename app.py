from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")

client.admin.command("ping")

print("MD connected Successfully !")

db = client['flask_db']
users_collection = db["users"]

@app.route("/")
def home():
    return "Flask is working !"

@app.route("/add-user")
def add_user():
    user = {
        "name":"Mohit",
        "email":"mohit@gmail.com",
        "age":30
    }
    result = users_collection.insert_one(user)
    return{
        "message":"User Inserted Successfully !",
        "id": str(result.inserted_id)
    }

if __name__ == "__main__":
    app.run(debug=True)
