from flask import request, session, redirect
from flask import render_template

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
            return render_template('dashboard.html')

dashboardController=DashboardController()
