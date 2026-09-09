from flask import Flask,render_template, request,redirect,url_for,flash,session

app = Flask(__name__)

app.secret_key = "change-this-in-prod"

@app.route("/login")
def login():
    session["username"]= "Mohit"
    return "Login Successful !"

@app.route("/deshboard")
def deshboard():
    username = session.get("username")
    if not username:
        return "Please Login First !"
    return f" Welcome, {username}"

@app.route("/logout")
def logout():
    session.pop("username",None)
    return "Logged Out !"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip()
        age = request.form.get("age","").strip()

        if not name:
            flash("Name is Required !","danger")
            return redirect(url_for("contact"))
        if not email:
            flash("Email is Required !","danger")
            return redirect(url_for("contact"))
        if not age:
            flash("Age is Required !","danger")
            return redirect(url_for("contact"))
        if not age.isdigit():
            return "Age Must be a Number"
        age = int(age)
        flash("Registration Successful !","success")
    return render_template("contact.html")

@app.route("/success")
def success():
    return "Registration Successful"

if __name__ == "__main__":
    app.run(debug=True)