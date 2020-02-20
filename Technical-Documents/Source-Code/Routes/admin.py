from flask import Blueprint,request,json
from flask import render_template
from Controllers.adminAuth import adminAuthController
from Controllers.game import gameController

# Author - Ben Constable
# Modified - Ravi Gohel
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

@admin.route('/admin/game/create', methods=['POST'])
def gameCreate():
    return gameController.createGame()

@admin.route('/admin/game/end', methods=['POST'])
def gameEnd():
    return gameController.endGame()

@admin.route('/admin/upload', methods=['POST'])
def uploadFile():
    return gameController.uploadFile()

@admin.route('/admin/register', methods=['POST'])
def registerAdmin():
    return adminAuthController.adminRegister()
