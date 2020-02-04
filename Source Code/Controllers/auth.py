from flask import request, session, redirect
from flask import render_template
from Models.teamModel import teamModel
from Helpers.utility import escapeInput

# Author - Ben Constable
# MVC Controller for handling user sign up
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

    """Handle the form for the registering

    :return: A redirect or a template. """
    def registerTeam(self):
        # Get the values from the request
        teamName = request.form.get('TeamName')
        gamePin = request.form.get('GamePin')

        # Get the response from the model
        response = teamModel.registerTeam(escapeInput(teamName), escapeInput(gamePin))

        if response["status"] == "1":
            # Set the session variables
            session["loggedIn"] = "True"
            session["teamID"] = response["ID"]
            session["gamePin"] = response["gamePin"]
            session["subject"] = response["subject"]

            # Redirect
            return redirect("/dashboard", code=302)
        else:
            # Should output the error on the home template
            return render_template('home.html', status=response["status"], message=response["message"])

    """Handle the form for the logging on

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

            # Redirect
            return redirect("/dashboard", code=302)
        else:
            #should output the error
            return render_template('home.html', status=response["status"], message=response["message"])

authController=AuthController()