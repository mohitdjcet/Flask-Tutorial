from flask import Flask
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

@app.route("/")
def home():
    return "Flask application is running !"

@app.route("/db-test")
def db_test():
    result = db.session.execute(
        text("SELECT 1")
    )
    value = result.scalar()
    return f"MySQL connected Fine ! Result : {value}"

if __name__ == "__main__":
    app.run(debug=True)
