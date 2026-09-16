from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///app.db"

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable= False)
    email= db.Column(db.String(120),nullable= False)
    age= db.Column(db.Integer)

@app.route("/")
def home():
    return "Flask + SQLite + SQLAlchemy is working !"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)