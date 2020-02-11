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
            response = subjectModel.getSubjects()
            return render_template('game.html',status = response["status"],length = len(response["data"]),data = response["data"])

    def createGame(self):
        subjectID = request.form.get('SubjectID')
        keeperID = session.get("keeperID")
        print(keeperID)

        return gameModel.createGame(subjectID, keeperID)

    def allowedFile(self, filename):
        print(filename)
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'json'}

    def uploadFile(self):
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            print("error")
            return render_template('game.html')

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('game.html')
        if file and self.allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save("Configs/" + filename)

            return gameModel.processGameFile("Configs/" + filename)

gameController=GameController()
