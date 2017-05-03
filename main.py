from flask import Flask, request, render_template, redirect, url_for
import common

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    # data_table = common.get_table_from_file("data/question.csv")
    return render_template("index.html")


@app.route("/answer/<id>", methods=["GET", "POST"])
def answer(id):
    return render_template("answer.html",
                           question_title="Which color is my fav?",
                           message="Blue",
                           answer_list=["Its my good answer! asdasf sdfsdnsdfk  dksdf  klsd  jklsd jklsd éljkas  éksd géklsgéklsd géks éksdgéksgdklsd fgékfsdfgdf gsdj iljsdf kljsdfkljsdklfjsdf kl", "500", "2014.04.03"])


@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    return render_template("update.html")


if __name__ == '__main__':
    app.run(debug=True)
