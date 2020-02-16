import os
from flask import request, session, redirect, url_for
from flask import render_template
from Models.gameModel import gameModel
from Models.subjectModel import subjectModel
from werkzeug.utils import secure_filename
import json

# Author - Ben Constable
# MVC Controller for the game management page
class GameController():

    def __init__(self):
        pass

    """Handle the empty page.

    :return: A redirect or a template. """
    def index(self):
        # Check if logged in
        if not session.get('adminLoggedIn'):
            return redirect("/admin", code=302)
        else:
            #get all of the different subjects
            subjectResponse = subjectModel.getSubjects()

            #get the stored session data
            keeperID = session.get("keeperID")

            #get any active games for this keeper
            gameResponse = gameModel.getGames(keeperID, 1)

            #render the html
            if (len(gameResponse) == 0):
                return render_template('game.html',status = subjectResponse["status"],subjectLength = len(subjectResponse["data"]),subjectData = subjectResponse["data"],gameStatus = 0)
            else:
                return render_template('game.html',status = subjectResponse["status"],subjectLength = len(subjectResponse["data"]),subjectData = subjectResponse["data"],gameStatus = 1, gamePin = gameResponse[0]["GamePin"])

    """Handle starting of a game by a post request

    :return: A redirect or a template. """
    def createGame(self):
        #get the data from the form and session
        subjectID = request.form.get('SubjectID')
        keeperID = session.get("keeperID")

        return gameModel.createGame(subjectID, keeperID)

    """Handle ending of a game by a post request

    :return: A redirect or a template. """
    def endGame(self):
        #get the data from the session
        keeperID = session.get("keeperID")

        return gameModel.endGame(keeperID)

    """Handle ending of a game by a post request

    :param filename: The name of the file being uploaded

    :return: A boolean value showing if the file type is allowed. """
    def allowedFile(self, filename):
        #split out the file and check the ending against the allowed types
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'json'}

    """Handle uploading of a game over AJAX

    :return: A redirect or a template. """
    def uploadFile(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            return {'status':'0', 'message':'Invalid type of request.'}

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'status':'0', 'message':'You must select a file!'}
            
        if file and self.allowedFile(file.filename):

            #get a legal file name for it
            filename = secure_filename(file.filename)

            #save the file for later
            file.save("Configs/" + filename)

            #process it
            return gameModel.processGameFile("Configs/" + filename)

gameController=GameController()
