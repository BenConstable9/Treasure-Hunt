from flask import request,json
import sqlite3 as sql
import json

# Author - Ravi Gohel, Ben Constable
# MVC Model for handling user pin

class SubjectModel():
    def __init__(self):
        pass

    """Create a subject given subject details

    :param subjectName: The subject name.
    :param building: The name of the building.
    :param longitude: The longitude of the building.
    :param latitude: The latitude of the building.

    :return:  A JSON array with status."""
    def createSubject(self, subjectName, building, longitude, latitude):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                # See if the username exists
                cur.execute("SELECT * FROM Subjects WHERE SubjectName=?", (subjectName,))

                otherSubjects = cur.fetchall()

                #now check the subject is not already taken
                if (len(otherSubjects) == 0):
                    #shuld we overwite existing configs>

                    # Insert the team data
                    cur.execute("INSERT INTO Subjects (SubjectName,Building,Longitude,Latitude) VALUES (?,?,?,?)",(subjectName,building,longitude,latitude) )

                    con.commit()

                    # Get the last id
                    lastID = cur.lastrowid

                    response = {'status':'1', 'message':'Subject Creation Successfull', 'ID': lastID}

                else:
                    response = {'status':'0', 'message':'Subject Creation Unsuccessful - Name Already Taken. Please Delete Subject Then Try Again.', 'ID': '0'}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()


    """Obtain details of subjects

    :return:  A JSON array with status."""
    def getSubjects(self):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                # See if the username exists
                cur.execute("SELECT * FROM Subjects")

                subjects = cur.fetchall()

                returns = []

                for subject in subjects:
                    returns.append({"SubjectID":subject["SubjectID"], "SubjectName":subject["SubjectName"], "Building":subject["Building"]})

                response = {'status':'1', 'message':'Collected subjects', 'data': returns}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:

            # Return the result
            return response

            con.close()

    """Verifies a pin

    :param gamePin: the given gamePin.

    :return: A JSON array response with the status. """
    def verifyPin(self, gamePin):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                #map the columns to the rows
                con.row_factory = sql.Row
                cur = con.cursor()

                #Get the subject associated with that GamePin
                cur.execute ("""
                    SELECT *
                    FROM Subjects
                    INNER JOIN Games
                    ON Subjects.SubjectID = Games.SubjectID
                    WHERE Games.GamePin = ? AND Games.Active='1'""",(gamePin,))
                game = cur.fetchall()
                for row in game:
                    subject = row[0]
                    obtained_row = row

                # Check the game pin
                if (gamePin == obtained_row["GamePin"]):
                    # Formulate the response
                    response = {'status':'1', 'message':'Team Logged In Successfully', 'subjectID': obtained_row["SubjectID"], 'subject': obtained_row["SubjectName"], 'gamePin': obtained_row["GamePin"]}

                else:
                    response = {'status':'0', 'message':'BAD - Invalid Game Pin', 'ID': '0'}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:
            # Return the result
            return response

            con.close()

    """Verifies a pin

    :param subjectID: The given unique subject ID.

    :return: A JSON array response with the status. """
    def getBuilding(self, subjectID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
            cur.execute("SELECT * FROM Subjects WHERE SubjectID=?", (int(subjectID),))

            subject = cur.fetchone()
            if (subject is not None):
                response = {'status':'1','building':subject["Building"]}
            else:
                response = {'status':'0'}
        except Exception as e:
            print(e)
            response = {'status':'0'}
        finally:
            # Return the result
            return response

            con.close()

subjectModel=SubjectModel()
