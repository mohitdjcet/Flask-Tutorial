from flask import (
    Flask,render_template,request,redirect,url_for,flash,abort
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,select
from sqlalchemy.exc import IntegrityError
from datetime import datetime,timezone

app = Flask(__name__)

app.config["SECRET_KEY"]= "change-this-for-local-dev"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)

#Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

#Validation and normalization form data
def get_student_data():
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip()
    course = request.form.get("course","").strip()
    phone = request.form.get("phone","").strip()

    if not all([name,email,course,phone]):
        return None, "All Fields are required"
    if len(name)> 100:
        return None, "Name must be 100 Chars or fewer."
    if len(email)>120 or "@" not in email:
        return None, "Please enter a valid email Id"
    if len(course)>100:
        return None, "Course must be 100 Chars or fewer."
    if len(phone)>20:
        return None, "Phone must be 20 Chars or fewer."

    return{
        "name":name,
        "email":email,
        "course":course,
        "phone":phone
    }, None

#List,search and pagination
@app.route("/")
def index():
    return redirect(url_for("list_students"))

@app.route("/students")
def list_students():
    q = request.args.get("q","").strip()
    page = request.args.get("page",1,type=int)
    per_page= 10
    if page is None or page < 1:
        page = 1
    stmt = select(Student)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(
            or_(
                Student.name.ilike(pattern),
                Student.email.ilike(pattern),
                Student.course.ilike(pattern)
            )
        )
    stmt = stmt.order_by(Student.id.desc())
    pagination = db.paginate(
        stmt,
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template(
        "students.html",
        pagination=pagination,
        students= pagination.items,
        q=q
    )


#Create Student
@app.route("/students/add", methods=["GET","POST"])
def add_student():
    if request.method == "POST":
        data,error = get_student_data()
        if error:
            flash(error,"danger")
            return render_template("student_form.html",student=None)
        student = Student(**data)
        db.session.add(student)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This Email Id is already registered","danger")
            return render_template("student_form.html",student=None)
        flash("Student Added Successfully","success")
        return redirect(url_for("list_students"))
    return render_template("student_form.html",student=None)

#Update Student
@app.route("/students/<int:student_id>/edit", methods= ["GET","POST"])
def edit_student(student_id):
    student = db.get_or_404(Student,student_id)
    if request.method == "POST":
        data,error = get_student_data()
        if error:
            flash(error,"danger")
            return render_template("student_form.html",student=student)
        for key, value in data.items():
            setattr(student,key,value)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This Email Id is already registered","danger")
            return render_template("student_form.html",student=student)
        flash("Student Updated Successfully","success")
        return redirect(url_for("list_students"))
    return render_template("student_form.html",student=student)

#Delete student
@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    student = db.get_or_404(Student,student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully !", "success")
    return redirect(url_for("list_students"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)