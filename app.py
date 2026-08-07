from flask import Flask
from uuid import UUID

app = Flask(__name__)

@app.route("/")
def home():
    return "Home Page"

@app.route("/user/<string:name>")
def user(name):
    return f"User ID: {name}"

@app.route("/price/<float:amount>")
def price(amount):
    return f"Price: {amount}"

@app.route("/files/<path:file_path>")
def files(file_path):
    return file_path

@app.route("/student/<uuid:user_id>")
def student(user_id):
    return str(user_id)

if __name__ == "__main__":
    app.run(debug=True)