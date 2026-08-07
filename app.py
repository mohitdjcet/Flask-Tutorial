from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Home Page"

@app.route("/users")
def users():
    return "Welcome to User Page"

@app.route("/user/<name>")
def user(name):
    return f"Hello {name}"

@app.route("/student/<name>/<course>")
def student(name,course):
    return f"{name} is lerning {course}"

if __name__ == "__main__":
    app.run(debug=True)