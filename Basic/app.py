from flask import Flask, request, render_template, redirect, flash, session
from surveys import Question, surveys, Survey, satisfaction_survey, personality_quiz
from random import choices


app = Flask(__name__)
app.config['SECRET_KEY'] = "dntKnow"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#       MAKING ROUTES

responses = []

@app.route('/')
def Home_page():
    '''Shows web HomePage'''
    title = satisfaction_survey.title

    instruction = satisfaction_survey.instructions

    return render_template('survey_page.html',title=title, givenInstr=instruction)

@app.route('/start', method=['POST'])
def start_survey():
    ''' Starts the survey '''

    return redirect('/questions/0')


@app.route('/questions/<int:q_num>')
def questions(q_num):
    
    if (responses is None):
        # Accessing questions without starting it.
        return redirect('/')
    
    if (len(responses)) == len(satisfaction_survey.questions):
        # If all questions are complete. Get a completion message.
        return redirect('/complete')
    
    if(len(responses) != q_num):
        flash(f'Invalid question number!')
        return redirect(f'/questions/{len(responses)}')
    
    if q_num >= len(satisfaction_survey.questions):
        return redirect('/complete')
    
    questions = satisfaction_survey.questions[q_num]

    return render_template('question.html', question=questions, q_num=q_num)


@app.route('/answers',methods=['POST'])
def get_answer():
    '''Get the question number form and its answer,also redirect to the next question '''

    ans = request.form('answer')

        # Stores answers
    responses.append(ans) 
   
        # All questions answered! Redirect to complete page.
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')
    
@app.route('/complete')
def complete():
    '''Returns a thank you note'''

    return 'Thanks you for completing the survey'
