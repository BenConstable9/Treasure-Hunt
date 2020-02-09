from flask import request,json
import sqlite3 as sql

# Author - Ravi Gohel, Ben Constable
# MVC Model for handling tutors

class TutorModel():
    def __init__(self):
        pass

    def createTutor(self, subjectID, name, room):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                # Insert the tutor data
                cur.execute("INSERT INTO Tutors (SubjectID,Name,Room) VALUES (?,?,?)",(subjectID,name,room) )

                con.commit()

                # Get the last id
                lastID = cur.lastrowid

                response = {'status':'1', 'message':'Tutor Creation Successfull', 'ID': lastID}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

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

tutorModel=TutorModel()
