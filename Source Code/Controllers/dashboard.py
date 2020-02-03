from flask import request, session, redirect
from flask import render_template

class DashboardController():

    def __init__(self):
        pass

    def index(self):
        if not session.get('LoggedIn'):
            return redirect("/", code=302)
        else:
            return render_template('dashboard.html')

dashboardcontroller=DashboardController()
