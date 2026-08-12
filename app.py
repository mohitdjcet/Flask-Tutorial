from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    first_name = "Rohit"
    last_name = "Kumar"
    city = "Delhi"
    price=500
    course= [
        "python",
        "Flask",
        "Django",
        "FastApi"
    ]
    return render_template("index.html", 
                        first_name=first_name,
                        last_name = last_name,
                        course=course,
                        city=city,
                        price=price)

if __name__ == "__main__":
    app.run(debug=True)