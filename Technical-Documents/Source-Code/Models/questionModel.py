from flask import request,json
from Helpers.utility import makeRowDictionary
import datetime
from Models.leaderboardModel import leaderboardModel
import sqlite3 as sql

# Author - Ravi Gohel
# Edited - Zach Lavender - getting and checking answers
# MVC Model for handling user pin

class QuestionModel():
    def __init__(self):
        pass

    """Create a question given the question details

    :param subjectID: The subject name.
    :param building: The name of the building.
    :param QRLocation: The QR Location.
    :param QRText: The QR text.
    :param question: The question to be asked.
    :param answer: The answer to the question.
    :param letter: The letter associated with the question for the hangman game.
    :param letterIndex: The index of the letter in the building word.
    :param longitude: The longitude.
    :param latitude: The latitude.

    :return:  A JSON array with status."""
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

# takes in a team id when the page is refresed gets and returns any of the letters for the questions they have answered.
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

# takes in the id of a team
# retures a json object with a 1 if they have completed the game and a 0 if they have not
# Uses the team name to check the length of the name of the building they need to get to if its the same as the number of correct answers theyve given then retuns that have won and sets there finish time
    def checkComplete(self, teamID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = makeRowDictionary
                cur = con.cursor()
                cur.execute("SELECT * FROM Teams Inner Join Subjects ON Teams.SubjectID = Subjects.SubjectID WHERE TeamID=?", (teamID,))
                Subject = cur.fetchone()
                building = Subject["Building"]
                cur.execute("SELECT * FROM Results where TeamID=?", (teamID,))
                results = cur.fetchone()
                numLetters = results["Letters"]
                if len(building) == numLetters:
                    cur.execute("SELECT * FROM Teams Inner Join Tutors ON Teams.TutorID = Tutors.TutorID WHERE TeamID=?", (teamID,))
                    results = cur.fetchone()
                    cur.execute("UPDATE Results SET FinishTime = ? WHERE TeamID = ?",(datetime.datetime.now(),teamID))
                    con.commit()
                    room = results["Room"]
                    return {'status': '1', 'room': room}
                else:
                    return {'status':'0'}
        except Exception as e:
            print(e)
            return {'status':'0'}
        finally:
            # Return the result

            con.close()

# takes the answers to a question the id of that question and the teamId of the team answering the question
# returns a json object with varing status depending if there answer was correct or if they have won the game. Inside the object is the letters they have collected the bulding they were in and the question id of the question they QuestionsAnswered
# checks there answers agains the one in the database for a given question id. also calls to check if they have completed the game if there answer was correct
    def checkAnswer(self,answer,questionId,teamID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = makeRowDictionary
                cur = con.cursor()

                cur.execute("SELECT * FROM Questions WHERE QuestionID=?", (questionId,))

                question = cur.fetchone()
                #checks if the given answers is the one in the database - with any capitals ignored
                if str(question["Answer"].casefold()) == str(answer.casefold()):
                    cur.execute("SELECT * FROM QuestionsAnswered WHERE QuestionID=? AND TeamID=?", (questionId,teamID))
                    result = cur.fetchone()
                    res = None
                    #if the question hasnt already been answered
                    if result is None:
                        #adds the fact that they have copleted the question to the db
                        cur.execute("INSERT INTO QuestionsAnswered VALUES (?,?,?)", (questionId,teamID,datetime.datetime.now()))
                        con.commit()
                        leaderboardModel.addLetter(teamID)
                        cur.execute("SELECT * FROM QuestionsAnswered Inner Join Questions ON QuestionsAnswered.QuestionID = Questions.QuestionID WHERE TeamID=?", (teamID,))

                        res = cur.fetchall()

                    if res is not None:
                        # for each question theve answered it adds the requred infomation to the output
                        returns = []
                        for let in res:

                            returns.append({"letter":let["Letter"], "building":let["Building"], "questionID":let["QuestionID"]})
                        #if they have completed the game then also returns the final room for them to go to
                        won = self.checkComplete(teamID)

                        if won["status"] == '1':
                            response = {'status': '2', 'data': returns, 'room' : won["room"]}
                        else:
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
