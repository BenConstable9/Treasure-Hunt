from flask import request,json
import sqlite3 as sql
import json
import hashlib
import random
from Models.subjectModel import subjectModel
from Models.tutorModel import tutorModel
from Models.questionModel import questionModel
from Helpers.utility import escapeInput

# Author - Ben Constable
# Modified - Ravi Gohel
# MVC Model for handling admin related data
class GameModel():
    def __init__(self):
        pass

    def createGame(self, subjectID, keeperID):
        print(subjectID)
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                gamePin = random.randint(100000, 999999)

                # Insert the team data
                cur.execute("INSERT INTO Games (SubjectID,GamePin,KeeperID,Active) VALUES (?,?,?,?)",(subjectID,gamePin,keeperID,1) )

                con.commit()

                # Get the last id
                lastID = cur.lastrowid

                response = {'status':'1', 'message':'Added game', 'ID': lastID, 'GamePin':gamePin}

        except Exception as e:
            print(e)
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
            with open(jsonFile, encoding="utf8") as file:
                contents = json.loads(file.read())

                #get a subject id
                subjectResponse = subjectModel.createSubject(escapeInput(contents["Subject"]), escapeInput(contents["FinalLoc"]["Building"]), escapeInput(contents["FinalLoc"]["GPS"][0]), escapeInput(contents["FinalLoc"]["GPS"][1]))
                print(subjectResponse)
                #MUST CHANGE THIS TO 1
                if (subjectResponse["status"] == "1"):
                    subjectID = subjectResponse["ID"]

                    #now add the tutors
                    print(contents["Tutors"])

                    for tutor in contents["Tutors"]:
                        print (tutor)
                        tutorModel.createTutor(subjectID, escapeInput(tutor["Name"]), escapeInput(tutor["Room"]))

                    if (len(contents["Locations"]) == len(contents["FinalLoc"]["Building"])):
                        randomBuilding = ''.join(random.sample(contents["FinalLoc"]["Building"],len(contents["FinalLoc"]["Building"])))

                        x = 0
                        for location in contents["Locations"]:
                            print (location)

                            QRText = hashlib.md5((location["Building"] + location["QRLocation"]).encode())
                            QRText = QRText.hexdigest()

                            questionResponse = questionModel.createQuestion(subjectID, escapeInput(location["Building"]), escapeInput(location["QRLocation"]), escapeInput(QRText), escapeInput(location["Question"]), escapeInput(location["Answer"]), escapeInput(randomBuilding[x]), escapeInput(location["GPS"][0]), escapeInput(location["GPS"][1]))

                            #here we should create and store the qr code with the value of QRText and name it the question id

                            x += 1

                        response = {'status':'0', 'message':'Game config added successfully.', 'ID': subjectID, 'Name': contents["Subject"], 'FinalLocation': contents["FinalLoc"]["Building"]}
                    else:
                        response = {'status':'0', 'message':'Game not added successfully - length of locations is not the same as the final building.', 'ID': '0'}

                else:
                    response = subjectResponse
        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'Unable to read in JSON file.', 'ID': '0'}

        finally:
            file.close()

            return response

gameModel=GameModel()
