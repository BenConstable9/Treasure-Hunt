from flask import request,json
import sqlite3 as sql

# Author - Ravi Gohel
# MVC Model for handling user pin

class QuestionModel():
    def __init__(self):
        pass

    def createQuestion(self, subjectID, building, QRLocation, QRText, question, answer, letter, letterIndex, longitude, latitude):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                # See if the username exists
                cur.execute("SELECT * FROM Subjects WHERE SubjectID=?", (subjectID,))

                subjects = cur.fetchall()

                #now check the username is not already taken
                if (len(subjects) == 1):
                    # Insert the team data
                    cur.execute("INSERT INTO Questions (SubjectID,Building,QRLocation,QRText,Question,Answer,Letter,LetterIndex,Longitude,Latitude) VALUES (?,?,?,?,?,?,?,?,?,?)",(subjectID,building,QRLocation,QRText,question,answer,letter,letterIndex,longitude,latitude) )

                    con.commit()

                    # Get the last id
                    lastID = cur.lastrowid

                    response = {'status':'1', 'message':'Question Creation Successfull', 'ID': lastID}

                else:
                    response = {'status':'0', 'message':'Question Creationn Unsuccessfull - Subject Already Taken', 'ID': '0'}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

    def verifyLocation(self, subjectID, qRText):
        try:
            print(qRText)
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur =  con.cursor()
                cur.execute("SELECT * FROM Questions WHERE QRText=?",(str(qRText),))

                questions =  cur.fetchall()
                returns =[]
                for question in questions:
                    returns.append({'QuestionID':question['Question']})
                response = {'status':'1','QuestionID': returns}
        except Exception as e:
            print(e)
            response = {'status':'0'}
        finally:

            #to be finished off
            return response
            con.close()

    def getQuestions(self, subjectID):
         try:
             # Open the DB
             with sql.connect("Models/treasure.sqlite") as con:
                 con.row_factory = sql.Row
                 cur = con.cursor()
                 cur.execute("SELECT * FROM Questions WHERE SubjectID=?", (int(subjectID),))

                 questions = cur.fetchall()
                 returns = []

                 for question in questions:
                     returns.append({"question":question["Question"], "answer":question["Answer"], "building":question["Building"],"letter":question["Letter"],"latitude":question["Latitude"],"longitude":question["Longitude"]})
                 response = {'status': '1', 'data': returns}
         except Exception as e:
             print(e)
             response = {'status':'0'}
         finally:
             # Return the result
             return response

             con.close()

    def checkAnswer(self,answer,questionId):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM Questions WHERE QuestionID=?", (int(questionId),))

                questions = cur.fetchall()
                returns = []

                for question in questions:
                    if question["Answer"] == answer:
                        returns.append({"letter":question["Letter"]})
                response = {'status': '1', 'data': returns}
        except Exception as e:
            print(e)
            response = {'status':'0'}
        finally:
            # Return the result
            return response

            con.close()

questionModel=QuestionModel()
