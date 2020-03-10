from flask import request,json
import sqlite3 as sql

# Author - Ravi Gohel, Ben Constable
# MVC Model for handling tutors

class TutorModel():
    def __init__(self):
        pass

    """Create a tutor for a given subject

    :param subjectID: The subjectID for the tutor.
    :param name: The name of the tutor to be added.
    :param room: The room the tutor will be located in.

    :return:  A JSON array with status."""
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

                response = {'status':'1', 'message':'Tutor Creation Successful', 'ID': lastID}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()


    """Obtains the list of tutors from a given subjectID

    :param subjectID: the given subjectID

    :return: A response. """
    def obtainTutors(self, subjectID):
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
                # For all tutors from the given subjectID, store their ID and Names
                for tutor in tutors:
                    listOfTutorIDs.append(tutor[0])
                    listOfTutorNames.append(tutor[2])

                #return the list to the user
                response = {'status':'1', 'message':'Obtained tutors', 'tutorIDs':listOfTutorIDs, 'tutorNames':listOfTutorNames}


        except:
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

tutorModel=TutorModel()
