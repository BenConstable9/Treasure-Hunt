from flask import Blueprint,request,json
from flask import render_template
from Controllers.adminAuth import adminAuthController
from Controllers.game import gameController

# Author - Ben Constable
# MVC Router for handling all admin related routes

admin = Blueprint("admin", __name__)

# Define all of the routes to be handled on the front end
@front.route('/admin', methods=['GET'])
def home():
    return adminAuthController.index()

@front.route('/admin/login', methods=['POST'])
def loginTeam():
    return adminAuthController.loginAdmin()

@front.route('/admin/login', methods=['POST'])
def loginTeam():
    return gameController.index()
