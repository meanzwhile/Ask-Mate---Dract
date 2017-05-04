from flask import Flask, request, render_template, redirect, url_for, abort
import common
from time import time
import datetime
app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/index/")
@app.route("/index/<sorting_col>/<way>")
def index(sorting_col=1, way="desc"):
    answers = common.get_table_from_file("data/answer.csv")
    table = common.get_table_from_file("data/question.csv")
    answer_counter = {}
    for element in table:
        table[table.index(element)].append(0)
        for value in answers:
            if element[0] == value[3]:
                table[table.index(element)][7] += 1
    if sorting_col is not None:
        table = common.sort_table(table, sorting_col, way)
    return render_template("index.html", question_list=table)


@app.route("/submit-question", methods=["POST"])
def submit_question():
    if "SLY" in request.form["question_title"]:
        return render_template("sly.html")
    table = common.get_table_from_file("data/question.csv")
    submit_data_list = []
    VIEW_NUMBER = "0"
    VOTE_NUMBER = "0"
    IMG_PATH = ""
    ID = common.ID_generator(table)
    submit_data_list.append(ID)
    timestamp = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    submit_data_list.append(timestamp)
    submit_data_list.append(VIEW_NUMBER)
    submit_data_list.append(VOTE_NUMBER)
    submit_data_list.append(request.form["question_title"])
    submit_data_list.append(request.form["message"])
    submit_data_list.append(IMG_PATH)
    table.append(submit_data_list)
    common.write_table_to_file(table, "data/question.csv")
    return redirect(url_for("index"))


@app.route("/answer/<question_id>")
@app.route("/answer/<question_id>/<sorting_col>/<way>")
def answer(question_id, sorting_col=2, way="desc"):
    QUESTION_ID = 3
    question_table = common.get_table_from_file("data/question.csv")
    actual_question = ""
    for element in question_table:
        if element[0] == question_id:
            actual_question = element
    table = common.get_table_from_file("data/answer.csv")
    answers_table = []
    for element in table:
        if element[QUESTION_ID] == question_id:
            answers_table.append(element)
    answers_table = common.sort_table_answer(answers_table, sorting_col, way)
    return render_template("answer.html", answers=answers_table, question=actual_question, question_id=question_id)


@app.route("/view/<question_id>")
def view_func(question_id):
    question_table = common.get_table_from_file("data/question.csv")
    for element in question_table:
        if element[0] == question_id:
            views = int(element[2]) + 1
            question_table[question_table.index(element)][2] = str(views)
            common.write_table_to_file(question_table, "data/question.csv")
    return redirect(url_for('answer', question_id=question_id))


@app.route("/submit-answer/<question_id>", methods=["POST"])
def submit_answer(question_id):
    answers = common.get_table_from_file("data/answer.csv")
    new_answer = []
    timestamp = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    new_answer.append(common.ID_generator(answers))
    new_answer.append(timestamp)
    new_answer.append("0")
    new_answer.append(question_id)
    new_answer.append(request.form["answer"])
    new_answer.append("IMAGE")
    answers.append(new_answer)
    common.write_table_to_file(answers, "data/answer.csv")
    return redirect(url_for('answer', question_id=question_id))


@app.route("/update/<question_id>", methods=["GET"])
def update_page(question_id):
    ID_INDEX = 0
    question_table = common.get_table_from_file("data/question.csv")
    data_to_fill = []
    for element in question_table:
        if element[ID_INDEX] == question_id:
            data_to_fill.append(element)
    return render_template("update.html", datas=data_to_fill)


@app.route("/submit-update/<question_id>", methods=["POST"])
def update_data(question_id):
    question_table = common.get_table_from_file("data/question.csv")
    updated_question = []
    for element in question_table:
        if element[0] == question_id:
            updated_question.append(element)
            question_table.remove(element)
    flatten_updated_question = []
    for element in updated_question:
        for item in element:
            flatten_updated_question.append(item)
    flatten_updated_question.pop(4)
    flatten_updated_question.pop(4)
    flatten_updated_question.insert(4, request.form['updated-question_title'])
    flatten_updated_question.insert(5, request.form['updated-message'])
    question_table.append(flatten_updated_question)
    common.write_table_to_file(question_table, "data/question.csv")
    return redirect(url_for('answer', question_id=question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    question_table = common.get_table_from_file("data/question.csv")
    answer_table = common.get_table_from_file("data/answer.csv")
    ID_INDEX = 0
    for element in question_table:
        if element[ID_INDEX] == question_id:
            question_table.remove(element)
    temp_table = []
    for question_id_old in answer_table:
        if question_id_old[3] != question_id:
            temp_table.append(question_id_old)
    common.write_table_to_file(question_table, "data/question.csv")
    common.write_table_to_file(temp_table, "data/answer.csv")
    return redirect(url_for("index"))


@app.route("/<question_id>/answer/<answer_id>/delete")
def delete_answer(answer_id, question_id):
    answer_table = common.get_table_from_file("data/answer.csv")
    for element in answer_table:
        if element[0] == answer_id:
            answer_table.remove(element)
    common.write_table_to_file(answer_table, "data/answer.csv")
    return redirect(url_for('answer', question_id=question_id))
    # return render_template("answer.html",  question_id=question_id)


@app.route("/answer/<question_id>/<element_id>/vote_up")
def vote_up_answer(question_id, element_id):
    common.general_vote_up(element_id, "data/answer.csv", 2)
    return redirect(url_for("answer", question_id=question_id))


@app.route("/answer/<question_id>/<element_id>/vote_down")
def vote_down_answer(question_id, element_id):
    common.general_vote_down(element_id, "data/answer.csv", 2)
    return redirect(url_for("answer", question_id=question_id))


@app.route("/index/vote_up/<element_id>")
def vote_up(element_id):
    common.general_vote_up(element_id, "data/question.csv", 3)
    return redirect(url_for("index"))


@app.route("/index/vote_down/<element_id>")
def vote_down(element_id):
    common.general_vote_down(element_id, "data/question.csv", 3)
    return redirect(url_for("index"))


@app.errorhandler(404)
def error_hadler(e):
    return render_template("handler.html")

if __name__ == '__main__':
    app.run(debug=True)
