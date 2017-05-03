from flask import Flask, request, render_template, redirect, url_for
import common

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    table = common.get_table_from_file("data/question.csv")
    return render_template("index.html", question_list=table)


@app.route("/", methods=["POST"])
@app.route("/index", methods=["POST"])
def submit_question():
    return render_template("index.html")


@app.route("/answer/<question_id>")
def answer(question_id):
    QUESTION_ID = 3
    question_table = common.get_table_from_file("data/question.csv")
    for element in question_table:
        if element[0] == question_id:
            actual_question = element
    table = common.get_table_from_file("data/answer.csv")
    answers_table = []
    for element in table:
        if element[QUESTION_ID] == question_id:
            answers_table.append(element)
    return render_template("answer.html", answers=answers_table, question=actual_question)


@app.route("/answer/<question_id>", methods=["POST"])
def submit_answer(question_id):
    answers = common.get_table_from_file("data/question.csv")
    new_answer = []
    new_answer.append(common.ID_generator(answers))
    new_answer.append()

    answers.append(new_answer)
    return render_template("answer.html")


@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    return render_template("update.html")


if __name__ == '__main__':
    app.run(debug=True)
