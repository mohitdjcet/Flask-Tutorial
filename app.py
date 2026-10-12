from flask import Flask,jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(200),
        nullable=False
    )
    completed = db.Column(
        db.Boolean,
        default=False
    )
    def __repr__(self):
        return f"<Todo {self.title}>"

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/todos",methods=["POST"])
def add_todos():
    data = request.get_json(silent=True) or {}
    title = data.get("title").strip()
    if not title:
        return({
            "message":"Title is required !"
        }),400
    todo = Todo(
        title = title
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        "message":"Todo added Succesfully !",
        "todo":{
            "id":todo.id,
            "title":todo.title,
            "completed":todo.completed
        }
    }),201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = db.session.get(Todo,todo_id)
    if not todo:
        return jsonify({
            "message":"Todo not found"
        }),404
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    completed = data.get("completed")

    if title is not None:
        title = title.strip()
        if not title:
            return jsonify({
                "message":"Title cannot be empty"
            }),400
        todo.title = title


    if completed is not None:
        if not isinstance(completed,bool):
            return jsonify({
                "message":"Completed must be True or False"
            }),400
        todo.completed = completed

    db.session.commit()
    return jsonify({
        "message":"Todo Updated Successfully !",
        "todo":{
            "id":todo.id,
            "title":todo.title,
            "completed":todo.completed
        }
    }),200

@app.route("/todos", methods=["GET"])
def get_todos():
    todos = db.session.execute(
        db.select(Todo).order_by(Todo.id.desc())
    ).scalars().all()
    return jsonify({
        "todos":[
            {
                "id":todo.id,
                "title":todo.title,
                "completed":todo.completed
            }
            for todo in todos
        ]
    }),200

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.session.get(Todo,todo_id)
    if not todo:
        return jsonify({
            "message":"TODO not found"
        }),404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({
        "message":"Todo deleted Successfully"
    }),200

if __name__ == "__main__":
    app.run(debug=True)