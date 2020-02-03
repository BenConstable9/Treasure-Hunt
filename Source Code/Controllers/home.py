from flask import request, session, redirect
from flask import render_template
from Models.teamModel import teamModel

class HomeController():

    def __init__(self):
        pass

    def index(self):
        if not session.get('LoggedIn'):
            return render_template('home.html')
        else:
            return redirect("/dashboard", code=302)

    def registerTeam(self):
        TeamName = request.form.get('TeamName')
        Subject = request.form.get('Subject')

        #todo check values and change the password
        Password = "Test"

        response = teamModel.registerTeam(TeamName, Password, Subject)
        print(response["Status"])

        if response["Status"] == "1":
            session["LoggedIn"] = "True"
            session["TeamID"] = response["ID"]
            return redirect("/dashboard", code=302)
        else:
            #handle the error
            print("broken")

            #should output the error

            return render_template('home.html')

    def loginTeam(self):
        return sendResponse(authmodel.registerUser(_firstname,_lastname,_email,_password))

homecontroller=HomeController()
