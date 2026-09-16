from flask import Flask,request,jsonify,render_template
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

@app.route("/create-user", methods=["POST"])
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
    })

@app.route("/get-user", methods=["GET"])
def get_users():
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "age":user.age
        })
    return jsonify(users_data)

@app.route("/users1")
def users():
    users = User.query.all()
    return render_template("user.html",users=users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.get_or_404(User,id)
    return jsonify({
        "id":user.id,
        "name":user.name,
        "email":user.email,
        "age":user.age
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)