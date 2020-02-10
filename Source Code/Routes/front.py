from flask import Blueprint,request,json
from flask import render_template
from Controllers.auth import authController
from Controllers.dashboard import dashboardController

# Author - Ben Constable
# MVC Router for handling all front end routes

front = Blueprint("front", __name__)

# Define all of the routes to be handled on the front end
@front.route('/', methods=['GET'])
def home():
    return authController.index()

@front.route('/register', methods=['POST'])
def registerTeam():
    return authController.registerTeam()

@front.route('/verifyPin', methods=['GET'])
def verifyPin():
    return authController.verifyPin()

@front.route('/login', methods=['POST'])
def loginTeamPost():
    return authController.loginTeam()

@front.route('/register', methods=['GET'])
def registerTeamGet():
    return authController.index()

@front.route('/login', methods=['GET'])
def loginTeamGet():
    return authController.index()

@front.route('/dashboard', methods=['GET'])
def fetchDash():
    return dashboardController.index()
