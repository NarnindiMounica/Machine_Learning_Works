from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("predictdata", methods=['GET', 'POST'])
def predict_datapoint():
    if request.method=="GET":
        return render_template("home.html")
    else:
        pass
