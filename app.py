from flask import Flask,render_template, request,redirect,url_for,flash,session
import os
from dotenv import load_dotenv
from users.routes import users_bp
from products.routes import products_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)

@app.route("/")
def home():
    return "Home"

if __name__ == "__main__":
    app.run(debug=True)