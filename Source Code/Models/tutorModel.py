from flask import request,json
import sqlite3 as sql

# Author - Ravi Gohel
# MVC Model for handling tutors

class TutorModel():
    def __init__(self):
        pass


    """Obtains the tutors from the given subject

    :return: A JSON array with the tutors. """
    def obtainTutors(self, subjectID):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                print ("SubjectID ting: ", subjectID)

                # Get the tutors name
                cur.execute("SELECT * FROM Tutors WHERE SubjectID=?", (subjectID,))
                tutors = cur.fetchall()
                listOfTutorIDs = []
                listOfTutorNames = []
                for tutor in tutors:
                    print (tutor[0])
                    listOfTutorIDs.append(tutor[0])
                    print (tutor[1])
                    print (tutor[2])
                    listOfTutorNames.append(tutor[2])
                    print (tutor[3])
                print (listOfTutorIDs)
                print (listOfTutorNames)


                response = {'status':'1', 'message':'Obtained tutors', 'tutorIDs':listOfTutorIDs, 'tutorNames':listOfTutorNames}


        except:
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

tutorModel=TutorModel()
