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
        name = request.form.get("username")
        return f"Hello , {name}"
    return render_template("contact.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    return f" You searched for : {query}"

if __name__ == "__main__":
    app.run(debug=True)