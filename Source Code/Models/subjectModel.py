from flask import request,json
import sqlite3 as sql
import json

# Author - Ravi Gohel, Ben Constable
# MVC Model for handling user pin

class SubjectModel():
    def __init__(self):
        pass

    def createSubject(self, subjectName, building, longitude, latitude):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                # See if the username exists
                cur.execute("SELECT * FROM Subjects WHERE SubjectName=?", (subjectName,))

                otherSubjects = cur.fetchall()

                #now check the username is not already taken
                if (len(otherSubjects) == 0):
                    #shuld we overwite existing configs>

                    # Insert the team data
                    cur.execute("INSERT INTO Subjects (SubjectName,Building,Longitude,Latitude) VALUES (?,?,?,?)",(subjectName,building,longitude,latitude) )

                    con.commit()

                    # Get the last id
                    lastID = cur.lastrowid

                    response = {'status':'1', 'message':'Subject Creation Successfull', 'ID': lastID}

                else:
                    response = {'status':'0', 'message':'Subject Creation Unsuccessfull - Subject Already Taken', 'ID': '0'}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

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
    :return: A JSON array with the status. """
    def verifyPin(self, gamePin):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()
                cur.row_factory = sql.Row
                print ("Gamepin: ", gamePin)

                # Get the team name
                cur.execute("SELECT * FROM Subject WHERE GamePin=?", (gamePin,))

                verified = cur.fetchone()

                print (verified)

                # Check the game pin
                if (gamePin == team["GamePin"]):

                    # Formulate the response
                    response = {'status':'1', 'message':'Team Logged In Successfully', 'ID': team["TeamID"], 'subject': team["Subject"], 'gamePin': team["GamePin"]}

                else:
                    response = {'status':'0', 'message':'BAD - Invalid Game Pin', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

subjectModel=SubjectModel()
