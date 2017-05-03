from flask import Flask, request, render_template, redirect, url_for
import common

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    table = common.get_table_from_file()
    return render_template("index.html", question_list=table)


@app.route("/", methods=["POST"])
@app.route("/index", methods=["POST"])
def submit_question():
    return render_template("index.html")


@app.route("/answer/<id>")
def answer(id):
    QUESTION_ID = 3
    question_table = common.get_table_from_file()
    for element in question_table:
        if element[0] == id:
            actual_question = element
    table = common.get_table_from_file("data/answer.csv")
    answers_table = []
    for element in table:
        if element[QUESTION_ID] == id:
            answers_table.append(element)
    return render_template("answer.html", answers=answers_table, question=actual_question)


@app.route("/answer/<id>", methods=["POST"])
def submit_answer(id):
    return render_template("answer.html")


@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    return render_template("update.html")


if __name__ == '__main__':
    app.run(debug=True)
