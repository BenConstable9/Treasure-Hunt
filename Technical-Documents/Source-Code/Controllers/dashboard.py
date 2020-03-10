from flask import request, session, redirect
from flask import render_template
from Models.subjectModel import subjectModel
from Models.leaderboardModel import leaderboardModel
from Models.questionModel import questionModel
from Models.leaderboardModel import leaderboardModel
from Models.gameModel import gameModel
from Helpers.utility import escapeInput
from Models.teamModel import teamModel
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

    """Loads the privacy webpage.

    :return: The html page"""
    def privacyPolicy(self):
        return render_template('privacypolicy.html')

    """Loads the leaderboard webpage.

    :return: The html page"""
    def leaderboard(self):
        return render_template('leaderboard.html')

    """Loads the scores for the leaderboard in that game

    :return: An array of the data."""
    def leaderboardData(self):
        #check if they are an admin or not by looking at referrrer
        if ("admin" in request.referrer):
            #get their details and find their active game
            keeperID = session.get("keeperID")
            gameResponse = gameModel.getGames(keeperID, 1)
            #handle them not having an active game
            if (len(gameResponse) == 1):
                gamePin = gameResponse[0]["GamePin"]
            else:
                return {'status':'0', 'message':'No Scores'}
        else:
            #they are player so get the data from the session
            gamePin = session.get('gamePin')

        #get the leaderboard data from the DB
        leaderboardResponse = leaderboardModel.obtainResults(gamePin)

        #return array of scores.
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
        response = questionModel.checkAnswer(escapeInput(answer),escapeInput(questionId),escapeInput(teamID) )
        print(response)
        if response["status"] == "1":

            #leaderboardModel.addLetter(escapeInput(teamID),escapeInput(gamePin))
            data = response["data"]
            gameModel.logAction(gamePin, teamID, "answered question " + questionId + " successfully")

            #ajax call to say passed
        else:
            print("status was not 1")
            gameModel.logAction(gamePin, teamID, "attempted to answer question " + questionId + " successfully")
            #ajax call to say failed

        return response

    def getAnswers(self):
        teamID = session.get('teamID')
        response = questionModel.getAnswers(escapeInput(teamID))
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
