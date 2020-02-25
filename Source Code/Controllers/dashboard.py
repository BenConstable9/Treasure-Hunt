from flask import request, session, redirect
from flask import render_template
from Models.subjectModel import subjectModel
from Models.questionModel import questionModel
from Helpers.utility import escapeInput
import random

# Author - Ben Constable, Zach Lavender
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
    def  building(self):
        return render_template('building.html')

    def lecturer(self):
        return render_template('lecturers.html')

    def faq(self):
        return render_template('FAQs.html')

    def openMap(self):
        return render_template('Map.html')


dashboardController=DashboardController()
