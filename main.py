from flask import Flask, request, render_template, redirect, url_for
import common
from time import time
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    table = common.get_table_from_file("data/question.csv")
    return render_template("index.html", question_list=table)


@app.route("/submit-question", methods=["POST"])
def submit_question():
    table = common.get_table_from_file("data/question.csv")
    submit_data_list = []
    VIEW_NUMBER = "0"
    VOTE_NUMBER = "0"
    IMG_PATH = ""
    ID = common.ID_generator(table)
    submit_data_list.append(ID)
    timestamp = str(int(time()))
    submit_data_list.append(timestamp)
    submit_data_list.append(VIEW_NUMBER)
    submit_data_list.append(VOTE_NUMBER)
    submit_data_list.append(request.form["question_title"])
    submit_data_list.append(request.form["message"])
    submit_data_list.append(IMG_PATH)
    print(submit_data_list)
    return redirect(url_for("index"))



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
