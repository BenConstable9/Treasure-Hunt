from flask import request, session, redirect
from flask import render_template
from Models.subjectModel import subjectModel
from Models.leaderboardModel import leaderboardModel
from Models.questionModel import questionModel
from Models.leaderboardModel import leaderboardModel
from Models.gameModel import gameModel
from Models.teamModel import teamModel
from Helpers.utility import escapeInput
import random

# Author - Ben Constable
# Edited - Zach lavender geting location oepning map, geting and checking answers
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
                random.shuffle(data)
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

    def privacyPolicy(self):
        return render_template('privacypolicy.html')

    def leaderboard(self):
        # Check if logged in
        if not session.get('loggedIn'):
            return redirect("/", code=302)
        else:
            return render_template('leaderboard.html')

    def leaderboardData(self):
        #get current game pin
        gamePin = session.get('gamePin')

        #get the leaderboard data from the DB
        leaderboardResponse = leaderboardModel.obtainResults(gamePin)

        return leaderboardResponse

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
        questionId = request.form.get("questionID")
        print("space1")
        response = questionModel.checkAnswer(escapeInput(answer.casefold()),escapeInput(questionId),escapeInput(teamID) )
        print("space2")
        print(response)
        if response["status"] == "0":
            gameModel.logAction(gamePin, teamID, "attempted to answer question " + questionId + " successfully")
            #ajax call to say failed

        else:
            #leaderboardModel.addLetter(escapeInput(teamID),escapeInput(gamePin))
            data = response["data"]
            gameModel.logAction(gamePin, teamID, "answered question " + questionId + " successfully")
            #ajax call to say passed

        return response

    def getAnswers(self):
        print("bigtest the one")
        teamID = session.get('teamID')
        response = questionModel.getAnswers(escapeInput(teamID))
        if response["status"] == "1":
            #leaderboardModel.addLetter(escapeInput(teamID),escapeInput(gamePin))
            data = response["data"]

            #ajax call to say passed
        else:
            #ajax call to say failed
            response = {}
        return response

    def getLoc(self):
        subject = session.get('subject')
        response = questionModel.getQuestions(escapeInput(subject))
        print("test")
        if response["status"] == "1":
            data = response["data"]
            random.shuffle(data)
            print(data)
            return response
        else:
            data = {"status" == "0"}
            return data

    """Request Help From Moderator"""
    def requestHelp(self):
        teamID = session.get('teamID')
        gamePin = session.get('gamePin')
        gameModel.logAction(gamePin, teamID, "requested help. Meet them at starting location.")


    """Allow the team to Logout """
    def teamLogout(self):
        response = teamModel.teamLogout()
        return response
dashboardController=DashboardController()
