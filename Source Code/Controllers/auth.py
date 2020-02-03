from flask import request, session, redirect
from flask import render_template
from Models.teamModel import teamModel

# Author - Ben Constable
# MVC Controller for handling user sign up
class AuthController():

    def __init__(self):
        pass

    def index(self):
        if not session.get('loggedIn'):
            return render_template('home.html')
        else:
            return redirect("/dashboard", code=302)

    def registerTeam(self):
        teamName = request.form.get('TeamName')
        gamePin = request.form.get('GamePin')

        #todo check values

        response = teamModel.registerTeam(teamName, gamePin)
        print(response["status"])

        if response["status"] == "1":
            session["loggedIn"] = "True"
            session["teamID"] = response["ID"]
            session["gamePin"] = response["gamePin"]
            session["subject"] = response["subject"]
            return redirect("/dashboard", code=302)
        else:
            #should output the error

            return render_template('home.html', status=response["status"], message=response["message"])

    def loginTeam(self):
        teamName = request.form.get('TeamName')
        gamePin = request.form.get('GamePin')

        response = teamModel.loginTeam(teamName, gamePin)

        if response["status"] == "1":
            session["loggedIn"] = "True"
            session["teamID"] = response["ID"]
            session["gamePin"] = response["gamePin"]
            session["subject"] = response["subject"]
            return redirect("/dashboard", code=302)
        else:
            #should output the error

            return render_template('home.html', status=response["status"], message=response["message"])

authController=AuthController()
