# First we must import Flask
# and by importing a flask object called request 
from flask import Flask, request, render_template, redirect, flash

#importing surveys.py
import surveys

#  Importing the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension

# This command initiates server - tells flask to do it's thing in the file.
app = Flask(__name__)

# Secret key for some reason
app.config['SECRET_KEY'] = "george_costanza"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

current_user_question_index = 0

@app.route('/')
def home_page():
    survey_title = surveys.satisfaction_survey.title
    return render_template('root.html', survey_title=survey_title, index=current_user_question_index)

@app.route('/questions/<int:questidx>')
def question(questidx):

    global current_user_question_index

    if questidx != current_user_question_index:
        flash('Please answer the current question')
        return redirect(f'/questions/{current_user_question_index}')

    survey_question = surveys.satisfaction_survey.questions[questidx].question
    survey_choices = surveys.satisfaction_survey.questions[questidx].choices

    return render_template('question_page.html',
    this_question=questidx,
    survey_choices=survey_choices,
    question=survey_question)

@app.route('/answer', methods=['POST'])
def answer():

    global current_user_question_index

    if request.form == {}:
        flash('Please answer the current question.')
        return redirect(f'/questions/{current_user_question_index}')

    answer = request.form['options']
    responses.append(answer)

    current_user_question_index += 1

    if current_user_question_index + 1 > len(surveys.satisfaction_survey.questions):
        return redirect('/thankyou')

    return redirect(f'/questions/{current_user_question_index}')

@app.route('/thankyou')
def thankyou():
    print(responses)

    if current_user_question_index + 1 < len(surveys.satisfaction_survey.questions):
        flash('Please answer the current question')
        return redirect(f'/questions/{current_user_question_index}')

    return render_template('thankyou.html')
