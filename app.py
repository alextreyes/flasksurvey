from flask import Flask, render_template, request, redirect, session, flash
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


responses = []

@app.route("/")
def home():
    return render_template('home.html', title=survey.title)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/begin", methods=["POST"])
def begin():
    session[RESPONSES_KEY] =[]
    return redirect("/questions/0")

# @app.route("/questions/<int:question_number>")
# def question(question_number):
#     question = survey.questions[question_number]
#     if ()
#     return render_template("question.html", question=question, question_number=question_number)

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    return render_template("completion.html")


