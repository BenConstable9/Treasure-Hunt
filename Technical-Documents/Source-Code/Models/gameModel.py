from flask import request,json
import sqlite3 as sql
import json
import hashlib
import random
import pyqrcode
import datetime
from Models.subjectModel import subjectModel
from Models.tutorModel import tutorModel
from Models.questionModel import questionModel
from Helpers.utility import escapeInput, makeRowDictionary

# Author - Ben Constable
# Modified - Ravi Gohel
# MVC Model for handling admin related data
class GameModel():
    def __init__(self):
        pass

    """Log an action for the admin to see.

    :param gamePin: The game you are currently playing.

    :param teamID: The team which is logging the action.

    :param action: A string describing the action they have just done. """
    def logAction(self, gamePin, teamID, action):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                # Insert the action
                cur.execute("INSERT INTO Notifications (GamePin,TeamID,Time,Action) VALUES (?,?,?,?)",(gamePin,teamID,datetime.datetime.now(),action))

                con.commit()

        except Exception as e:
            print(e)

        finally:

            con.close()

    """Get the latest actions for the admin.

    :param gamePin: The game pin of the game they are monitoring.

    :return: A dictionary of data to be returned via ajax. """
    def getNotifications(self, gamePin):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                #map the column names to the values returned
                con.row_factory = makeRowDictionary
                cur = con.cursor()

                #Get all of the notifications
                cur.execute("SELECT * FROM Notifications INNER JOIN Teams ON Notifications.TeamID = Teams.TeamID WHERE Notifications.GamePin=? ORDER BY Time DESC LIMIT 15", (gamePin,))

                results = cur.fetchall()

                response = {'status':'1', 'data':results}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:

            # Return the result
            return response

            con.close()

    """Handle creating of a game.

    :param subjectID: The subject to create the game for.

    :param keeperID: The keeper to assign the game to.

    :return: A json response which may contain a game pin. """
    def createGame(self, subjectID, keeperID):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = makeRowDictionary
                cur = con.cursor()

                #check they don't have any other games active
                otherGames = self.getGames(keeperID, 1)

                if (len(otherGames) == 0):
                    while (True):
                        #make a random game pin
                        gamePin = random.randint(100000, 999999)

                        #Get all of the games with the correct params
                        cur.execute("SELECT * FROM Games WHERE GamePin=?", (gamePin,))

                        matching = cur.fetchall()

                        if (len(matching) == 0):
                            # Insert the game data
                            cur.execute("INSERT INTO Games (SubjectID,GamePin,KeeperID,Active) VALUES (?,?,?,?)",(subjectID,gamePin,keeperID,1) )

                            con.commit()

                            # Get the last id
                            lastID = cur.lastrowid

                            response = {'status':'1', 'message':'Added game', 'ID': lastID, 'GamePin':gamePin}

                            break
                else :
                    response = {'status':'0', 'message':'You already have a game running.'}

        except Exception as e:
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:

            # Return the result
            return response

            con.close()


    """Get a list of all the games on the system.

    :param keeperID: The keeper to assign the game to.

    :param active: The state of the games to look for.

    :return: A json response containing a list of the games. """
    def getGames(self, keeperID, active):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                #map the column names to the values returned
                con.row_factory = makeRowDictionary
                cur = con.cursor()

                #Get all of the games with the correct params
                cur.execute("SELECT * FROM Games WHERE KeeperID=? AND Active=?", (keeperID,1))

                response = cur.fetchall()

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:

            # Return the result
            return response

            con.close()

    """Generates QR code for the questions.

    :param subjectID: The subject to generate the QR codes for.

    :return: A json response with details of the success. """
    def genQRCodes(self, subjectID):
        try:
            #Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                #Map the column names to the values returned
                con.row_factory = makeRowDictionary
                cur = con.cursor()

                #Get the question for the required building
                cur.execute("SELECT * FROM Questions WHERE SubjectID=?", (subjectID,))
                questions = cur.fetchall()

                for question in questions:
                    img = pyqrcode.create(question["QRText"])
                    img.svg("Static/Images/Codes/" + str(question["QuestionID"]) + ".svg", scale = 8)

                response = {'status':'1', 'message':'QR Codes Created'}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:

            # Return the result
            return response

            con.close()

    """Handle the deletion of a subject

    :param subjectID: The subject to be deleted.

    :return: A json response with details of the success."""
    def deleteSubject(self, SubjectID):
        try:
            #Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                #Delete the subject from the table
                cur.execute("DELETE FROM Questions WHERE SubjectID=?", (SubjectID))
                cur.execute("DELETE FROM Subjects WHERE SubjectID=?", (SubjectID))

                con.commit();

                response = {'status':'1', 'message':'Subject deleted successfully'}

        except Exception as e:
            #Incorrect Repsonse
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:

            # Return the result
            return response

            con.close()

    """Handle the ending of a game

    :param keeperID: The keeper to end the games assigned to.

    :return: A json response with details of the success. """
    def endGame(self, keeperID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                #End any active games by that keeper
                cur.execute("UPDATE Games SET Active=? WHERE KeeperID=? AND Active=?", (0,keeperID,1))

                response = {'status':'1', 'message':'Game ended successfully.'}

        except Exception as e:
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:

            # Return the result
            return response

            con.close()


    """Handle the uploading of a game file.

    :param: json - The JSON game file to parsed.

    :return: A JSON object containing the response."""
    def processGameFile(self, jsonFile):
        try:
            #open this file
            with open(jsonFile, encoding="utf8") as file:
                contents = json.loads(file.read())

                #get a subject id
                subjectResponse = subjectModel.createSubject(escapeInput(contents["Subject"]), escapeInput(contents["FinalLoc"]["Building"]), escapeInput(contents["FinalLoc"]["GPS"][0]), escapeInput(contents["FinalLoc"]["GPS"][1]))

                if (subjectResponse["status"] == "1"):
                    subjectID = subjectResponse["ID"]

                    #now add the tutors

                    for tutor in contents["Tutors"]:
                        #create each tutor
                        tutorModel.createTutor(subjectID, escapeInput(tutor["Name"]), escapeInput(tutor["Room"]))

                    #check each of the locations adds up the final
                    if (len(contents["Locations"]) == len(contents["FinalLoc"]["Building"])):
                        #shuffle the list
                        randomBuilding = ''.join(random.sample(contents["FinalLoc"]["Building"],len(contents["FinalLoc"]["Building"])))

                        x = 0
                        for location in contents["Locations"]:
                            #create a hash to store in the qr code
                            QRText = hashlib.md5((location["Building"] + location["QRLocation"]).encode())
                            QRText = QRText.hexdigest()

                            questionResponse = questionModel.createQuestion(subjectID, escapeInput(location["Building"]), escapeInput(location["QRLocation"]), escapeInput(QRText), escapeInput(location["Question"]), escapeInput(location["Answer"]), escapeInput(randomBuilding[x]), x, escapeInput(location["GPS"][0]), escapeInput(location["GPS"][1]))

                            x += 1

                        response = {'status':'1', 'message':'Game config added successfully.', 'SubjectID': subjectID, 'SubjectName': contents["Subject"], 'Building': contents["FinalLoc"]["Building"]}

                        self.genQRCodes(subjectID)
                    else:
                        #Incorrect Repsonse
                        response = {'status':'0', 'message':'Game not added successfully - length of locations is not the same as the final building.', 'ID': '0'}

                else:
                    response = subjectResponse
        except Exception as e:
            response = {'status':'0', 'message':'Unable to read in JSON file.', 'ID': '0'}

        finally:
            file.close()

            return response

gameModel=GameModel()
