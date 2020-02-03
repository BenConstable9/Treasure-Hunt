from flask import Blueprint,request,json
from flask import render_template
from Controllers.home import homecontroller
from Controllers.dashboard import dashboardcontroller

#Any for the front end

front = Blueprint("front", __name__)

@front.route('/', methods=['GET'])
def home():
    return homecontroller.index()

@front.route('/register', methods=['POST'])
def registerTeam():
    return homecontroller.registerTeam()

@front.route('/login', methods=['POST'])
def loginTeam():
    return homecontroller.loginTeam()

@front.route('/dashboard', methods=['GET'])
def fetchDash():
    return dashboardcontroller.index()
