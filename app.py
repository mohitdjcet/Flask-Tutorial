from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    name = "Rohit"
    course = "Flask"
    city = "Delhi"
    age:28
    return render_template("index.html", 
                           name=name,
                           course=course,
                           city=city,
                           age=28)

if __name__ == "__main__":
    app.run(debug=True)