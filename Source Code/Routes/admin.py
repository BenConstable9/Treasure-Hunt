from flask import Blueprint,request,json
from flask import render_template
from Controllers.adminAuth import adminAuthController
from Controllers.game import gameController

# Author - Ben Constable
# MVC Router for handling all admin related routes

admin = Blueprint("admin", __name__)

# Define all of the routes to be handled on the front end
@admin.route('/admin', methods=['GET'])
def adminHome():
    return adminAuthController.index()

@admin.route('/admin/login', methods=['POST'])
def loginAdmin():
    return adminAuthController.adminLogin()

@admin.route('/admin/game', methods=['GET'])
def gameAdmin():
    return gameController.index()
