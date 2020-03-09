from flask import request,json
from Helpers.utility import makeRowDictionary
import datetime
from Models.leaderboardModel import leaderboardModel
import sqlite3 as sql

# Author - Ravi Gohel
#Edited - zach lavender - geting and checking answers
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

                #now check the subject is in the db
                if (len(subjects) == 1):
                    # Insert the team data
                    cur.execute("INSERT INTO Questions (SubjectID,Building,QRLocation,QRText,Question,Answer,Letter,LetterIndex,Longitude,Latitude) VALUES (?,?,?,?,?,?,?,?,?,?)",(subjectID,building,QRLocation,QRText,question,answer,letter,letterIndex,longitude,latitude) )

                    con.commit()

                    # Get the last id
                    lastID = cur.lastrowid

                    response = {'status':'1', 'message':'Question Creation Successfull', 'ID': lastID}

                else:
                    response = {'status':'0', 'message':'Question Creation Unsuccessful - Subject Not In DB', 'ID': '0'}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

    def verifyLocation(self, subjectID, qRText):
        try:
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur =  con.cursor()
                cur.execute("SELECT * FROM Questions WHERE QRText=?",(str(qRText),))

                questions =  cur.fetchall()
                print(questions)

                if (len(questions) == 0):
                    response = {'status':'0', 'message':'Invalid QR Code - try scanning again.'}
                else:
                    question = questions[0]
                    response = {'status':'1','message':'QR Code Valid - You Have A New Question.', 'QuestionID': question['QuestionID'], 'Building': question['Building'],'Question': question['Question']}

        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'Unable to fetch question.'}
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
                     returns.append({"questionID":question["QuestionID"],"question":question["Question"], "answer":question["Answer"], "building":question["Building"],"letter":question["Letter"],"latitude":question["Latitude"],"longitude":question["Longitude"],"qrLocation":question["QRLocation"]})
                 response = {'status': '1', 'data': returns}
         except Exception as e:
             print(e)
             response = {'status':'0'}
         finally:
             # Return the result
             return response

             con.close()

    def getAnswers(self,teamID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                cur.execute("SELECT * FROM QuestionsAnswered Inner Join Questions ON QuestionsAnswered.QuestionID = Questions.QuestionID WHERE TeamID=?", (teamID,))
                result = cur.fetchall()
                if result is not None:
                    returns = []
                    for let in result:
                        returns.append({"letter":let["Letter"], "building":let["Building"], "questionID":let["QuestionID"]})
                    response = {'status': '1', 'data': returns}

        except Exception as e:
            print(e)
            response = {'status':'0'}
        finally:
            # Return the result
            return response
            con.close()

    def checkAnswer(self,answer,questionId,teamID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = makeRowDictionary
                cur = con.cursor()

                cur.execute("SELECT * FROM Questions WHERE QuestionID=?", (questionId,))

                question = cur.fetchone()

                if str(question["Answer"].casefold()) == str(answer.casefold()):
                    cur.execute("SELECT * FROM QuestionsAnswered WHERE QuestionID=? AND TeamID=?", (questionId,teamID))
                    result = cur.fetchone()
                    if result is None:

                        cur.execute("INSERT INTO QuestionsAnswered VALUES (?,?,?)", (questionId,teamID,datetime.datetime.now()))
                        con.commit()
                        leaderboardModel.addLetter(teamID)
                        cur.execute("SELECT * FROM QuestionsAnswered Inner Join Questions ON QuestionsAnswered.QuestionID = Questions.QuestionID WHERE TeamID=?", (teamID,))

                        res = cur.fetchall()

                    if res is not None:
                        returns = []
                        for let in res:

                            returns.append({"letter":let["Letter"], "building":let["Building"], "questionID":let["QuestionID"]})
                        response = {'status': '1', 'data': returns}
                else:
                    response = {'status':'0'}

        except Exception as e:
            print(e)
            response = {'status':'0'}
        finally:
            # Return the result
            return response

            con.close()

questionModel=QuestionModel()
