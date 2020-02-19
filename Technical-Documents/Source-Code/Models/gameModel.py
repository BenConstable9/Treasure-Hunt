from flask import request,json
import sqlite3 as sql
import json
import hashlib
import random
import pyqrcode
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

    """Handle creating of a game.

    :param subjectID: The subject to create the game for.

    :param keeperID: The keeper to assign the game to.

    :return: A json response which may contain a game pin. """
    def createGame(self, subjectID, keeperID):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                #check they don't have any other games active
                otherGames = self.getGames(keeperID, 1)

                if (len(otherGames) == 0):
                    #make a random game pin
                    gamePin = random.randint(100000, 999999)

                    # Insert the game data
                    cur.execute("INSERT INTO Games (SubjectID,GamePin,KeeperID,Active) VALUES (?,?,?,?)",(subjectID,gamePin,keeperID,1) )

                    con.commit()

                    # Get the last id
                    lastID = cur.lastrowid

                    response = {'status':'1', 'message':'Added game', 'ID': lastID, 'GamePin':gamePin}
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
    
    :return: The list of QR codes. """
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
                    print(question["QRText"])
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

                        response = {'status':'0', 'message':'Game config added successfully.', 'SubjectID': subjectID, 'SubjectName': contents["Subject"], 'Building': contents["FinalLoc"]["Building"]}

                        self.genQRCodes(subjectID)
                    else:
                        response = {'status':'0', 'message':'Game not added successfully - length of locations is not the same as the final building.', 'ID': '0'}

                else:
                    response = subjectResponse
        except Exception as e:
            response = {'status':'0', 'message':'Unable to read in JSON file.', 'ID': '0'}

        finally:
            file.close()

            return response

gameModel=GameModel()
