from flask import (
    Flask,render_template,request,redirect,url_for,flash,session
)
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import (
    generate_password_hash,check_password_hash
)

app = Flask(__name__)

app.config["SECRET_KEY"]= "change-this-for-local-dev"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)

#DB Models
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash= db.Column(db.String(255), nullable=False)
    notes = db.relationship(
        "Note",
        backref="author",
        cascade="all, delete-orphan"
    )

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.String(50), nullable=False, default="Personal"
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.now()
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )

#Custom Login Decorator
def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args,**kwargs):
        if "user_id" not in session:
            flash("Please login first,","warning")
            return redirect(url_for("login"))
        return view_function(*args,**kwargs)
    return wrapper

#Home
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("notes"))
    return redirect(url_for("login"))

#Registration
@app.route("/register", methods=["GET","POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("notes"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.","danger")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return render_template("register.html")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "warning")
            return render_template("register.html")

        user = User(
            name=name,
            email=email,
            password_hash= generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration Successfull! Please Login.","success")
        return redirect(url_for("login"))
    return render_template("register.html")

#Login
@app.route("/login",methods=["GET","POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("notes"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(
            user.password_hash,password
        ):
            session.clear()
            session["user_id"]= user.id
            flash("Welcome back","success")
            return redirect(url_for("notes"))
        flash("Invalid email or password","danger")
    return render_template("login.html")

#Logout
@app.route("/logout",methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("You have been logged out.","info")
    return redirect(url_for("login"))

#Notes+search+category
@app.route("/notes")
@login_required
def notes():
    search = request.args.get("q","").strip()
    category = request.args.get("category","").strip()
    query = Note.query.filter_by(
        user_id = session["user_id"]
    )
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            db.or_(
                Note.title.ilike(pattern),
                Note.content.ilike(pattern)
            )
        )
    if category:
        query = query.filter_by(category=category)

    all_categories = [
        row[0]
        for row in db.session.query(Note.category)
        .filter_by(user_id=session["user_id"])
        .distinct()
        .order_by(Note.category)
        .all()
    ]
    user_notes = query.order_by(
        Note.created_at.desc()
    ).all()
    return render_template(
        "notes.html",
        notes= user_notes,
        search=search,
        category=category,
        categories= all_categories
    )

#Create Notes
@app.route("/notes/add",methods=["GET","POST"])
@login_required
def add_note():
    if request.method == "POST":

        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "Personal").strip()

        if not title or not content:
            flash("Title and content are required.", "danger")
            return render_template("note_form.html", note=None)

        note = Note(
            title=title,
            content=content,
            category=(category or "Personal")[:50],
            user_id=session["user_id"]
        )

        db.session.add(note)
        db.session.commit()

        flash("Note created successfully!", "success")

        return redirect(url_for("notes"))

    return render_template("note_form.html", note=None)    

#Edit Notes

@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "Personal").strip()

        if not title or not content:
            flash("Title and content are required.", "danger")
            return render_template("note_form.html", note=note)

        note.title = title
        note.content = content
        note.category = (category or "Personal")[:50]

        db.session.commit()

        flash("Note updated successfully!", "success")

        return redirect(url_for("notes"))

    return render_template("note_form.html", note=note)

#Delete Notes
@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(note)
    db.session.commit()

    flash("Note deleted successfully.", "info")

    return redirect(url_for("notes"))

#Run App
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)