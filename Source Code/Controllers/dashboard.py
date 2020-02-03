from flask import request, session, redirect
from flask import render_template

# Author - Ben Constable
# MVC Controller for the home page
class DashboardController():

    def __init__(self):
        pass

    def index(self):
        if not session.get('loggedIn'):
            return redirect("/", code=302)
        else:
            return render_template('dashboard.html')

dashboardController=DashboardController()
