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
                con.row_factory = sql.Row
                cur = con.cursor()

                # Get the tutors name
                cur.execute("SELECT * FROM Tutors WHERE SubjectID=?", (subjectID,))
                tutors = cur.fetchall()
                listOfTutorIDs = []
                listOfTutorNames = []
                for tutor in tutors:
                    listOfTutorIDs.append(tutor[0])
                    listOfTutorNames.append(tutor[2])

                response = {'status':'1', 'message':'Obtained tutors', 'tutorIDs':listOfTutorIDs, 'tutorNames':listOfTutorNames}


        except:
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

tutorModel=TutorModel()
