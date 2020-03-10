from flask import request, session, redirect
from flask import render_template
from Models.subjectModel import subjectModel
from Models.teamModel import teamModel
from Models.tutorModel import tutorModel
from Helpers.utility import escapeInput
from Models.gameModel import gameModel

# Author - Ben Constable
# Modified By - Ravi Gohel
# MVC Controller for handling team sign up and logging in
class AuthController():

    def __init__(self):
        pass

    """Handle the empty page.

    :return: A redirect or a template. """
    def index(self):
        # Check if logged in
        if not session.get('loggedIn'):
            return render_template('home.html')
        else:
            return redirect("/dashboard", code=302)

    """Handle the form for the registering a team

    :return: A redirect or a template. """
    def registerTeam(self):
        # Get the values from the request
        teamName = request.form.get('TeamName')
        gamePin = request.form.get('GamePin')
        tutorID = request.form.get('TutorID')

        # Get the response from the model
        response = teamModel.registerTeam(escapeInput(teamName), escapeInput(gamePin), escapeInput(tutorID))

        if response["status"] == "1":
            # Set the session variables
            session["loggedIn"] = "True"
            session["teamID"] = response["ID"]
            session["gamePin"] = response["gamePin"]
            session["subject"] = response["subject"]
            session["tutor"] = response["tutor"]

            gameModel.logAction(gamePin, response["ID"], "registered for the game")
            # Redirect
            return redirect("/dashboard", code=302)
        else:
            # Should output the error on the home template
            return render_template('home.html', status=response["status"], message=response["message"])

    """Handle the form for the team logging in

    :return: A redirect or a template. """
    def loginTeam(self):
        # Get the values from the request
        teamName = request.form.get('TeamName')
        gamePin = request.form.get('GamePin')

        # Get the response from the model
        response = teamModel.loginTeam(escapeInput(teamName), escapeInput(gamePin))

        if response["status"] == "1":
            # Set the session varaibles
            session["loggedIn"] = "True"
            session["teamID"] = response["ID"]
            session["gamePin"] = response["gamePin"]
            session["subject"] = response["subject"]

            #log the action
            gameModel.logAction(gamePin, response["ID"], "logged back into the game")

            # Redirect
            return redirect("/dashboard", code=302)
        else:
            #should output the error
            return render_template('home.html', status=response["status"], message=response["message"])


    """Handle the form for checking the gamepin

    :return: tutors or a response"""
    def verifyPin(self):
        # Get the values from the request
        gamePin = request.args.get('GamePin')
        print (gamePin)
        # Get the response from the model
        response = subjectModel.verifyPin(escapeInput(gamePin))

        if response["status"] == "1":
            # Set the session varaibles
            session["gamePin"] = response["gamePin"]

            # Obtain the tutors
            tutors = tutorModel.obtainTutors(escapeInput(response["subjectID"]))
            return tutors
        else:
            return response


authController=AuthController()
