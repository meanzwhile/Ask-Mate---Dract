from flask import Flask, request, render_template, redirect, url_for
import common

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
