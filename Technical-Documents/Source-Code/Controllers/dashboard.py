from flask import request, session, redirect
from flask import render_template
from Models.subjectModel import subjectModel
from Models.questionModel import questionModel
from Models.leaderboardModel import leaderboardModel
from Helpers.utility import escapeInput
import random

# Author - Ben Constable
# MVC Controller for the home page
class DashboardController():

    def __init__(self):
        pass

    """Handle the empty page.

    :return: A redirect or a template. """
    def index(self):
        # Check if logged in
        if not session.get('loggedIn'):
            return redirect("/", code=302)
        else:
            teamID = session.get('teamID') #pass this to a model
            gamePin = session.get('gamePin')
            subject = session.get('subject')
            response = questionModel.getQuestions(escapeInput(subject))

            if response["status"] == "1":
                data = response["data"]
                return render_template('dashboard.html',info = data)
            else:
                return render_template('home.html')

    def verifyLocation(self):
        # Check if logged in
        if not session.get('loggedIn'):
            return {'status':'0', 'message':'Not Logged In - Refresh Page and Login'}
        else:
            subject = session.get('subject')
            value = request.form.get('value')
            return questionModel.verifyLocation(subject, value)

    def  building(self):
        return render_template('building.html')

    def lecturer(self):
        return render_template('lecturers.html')

    def faq(self):
        return render_template('FAQs.html')

    def openMap(self):
        if not session.get('loggedIn'):
            return redirect("/", code=302)
        else:
            teamID = session.get('teamID') #pass this to a model
            gamePin = session.get('gamePin')
            subject = session.get('subject')
            response = questionModel.getQuestions(escapeInput(subject))

            if response["status"] == "1":
                data = response["data"]
                random.shuffle(data)
                return render_template('map.html',info = data)
            else:
                return render_template('home.html')

    def checkAnswer(self):
        teamID = session.get('teamID')
        gamePin = session.get('gamePin')
        answer = request.form.get('answer')
        questionId = request.form.get('questionId')
        response = questionModel.checkAnswer(escapeInput(answer),escapeInput(questionId))
        if response["status"] == "1":
            leaderboardModel.addLetter(escapeInput(teamID),escapeInput(gamePin))
            letter = response["data"]

            #ajax call to say passed
        else:
            #ajax call to say failed
            response = {}
        return response

dashboardController=DashboardController()
