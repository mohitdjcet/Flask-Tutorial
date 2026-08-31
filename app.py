from flask import Flask,render_template, request

app = Flask(__name__)

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
            return "Name is Required"
        if not email:
            return "Email is Required"
        if not age:
            return "Age is Required"
        if not age.isdigit():
            return "Age Must be a Number"
        age = int(age)
        return "Registration Successfull"
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)