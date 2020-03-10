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

    """Verify the location by the QR code.

    :param subjectID: The subject ID.
    :param qRText: The text from the scanned QR code.

    :return:  A JSON array with status and question details."""
    def verifyLocation(self, subjectID, qRText):
        try:
            #Opens the database
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur =  con.cursor()
                #Find the question for the given QR code
                cur.execute("SELECT * FROM Questions WHERE QRText=?",(str(qRText),))

                questions =  cur.fetchall()

                #Checks if a question was found for the code
                if (len(questions) == 0):
                    response = {'status':'0', 'message':'Invalid QR Code - try scanning again.'}
                else:
                    question = questions[0]
                    response = {'status':'1','message':'QR Code Valid - You Have A New Question.', 'QuestionID': question['QuestionID'], 'Building': question['Building'],'Question': question['Question']}

        except Exception as e:
            #Error handling
            print(e)
            response = {'status':'0', 'message':'Unable to fetch question.'}
        finally:

            return response
            con.close()

    """Get the questions for the given subject.

    :param subjectID: The subject's unique ID.

    :return:  A JSON array with status and questions."""
    def getQuestions(self, subjectID):
         try:
             # Open the DB
             with sql.connect("Models/treasure.sqlite") as con:
                 con.row_factory = sql.Row
                 cur = con.cursor()
                 #Find all the questions for the given subject
                 cur.execute("SELECT * FROM Questions WHERE SubjectID=?", (int(subjectID),))

                 questions = cur.fetchall()
                 returns = []

                 #Appends all of the data from each of the questions to an array
                 for question in questions:
                     returns.append({"questionID":question["QuestionID"],"question":question["Question"], "answer":question["Answer"], "building":question["Building"],"letter":question["Letter"],"latitude":question["Latitude"],"longitude":question["Longitude"],"qrLocation":question["QRLocation"]})
                 response = {'status': '1', 'data': returns}
         except Exception as e:
            #Error handling
             print(e)
             response = {'status':'0'}
         finally:
             # Return the result
             return response

             con.close()

    """Get the answers for a given team.

    :param teamID: The team's unique ID.

    :return:  A JSON array with status and letters achieved."""
    def getAnswers(self,teamID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                #Find all the questions answered for the given team
                cur.execute("SELECT * FROM QuestionsAnswered Inner Join Questions ON QuestionsAnswered.QuestionID = Questions.QuestionID WHERE TeamID=?", (teamID,))
                result = cur.fetchall()

                #Checks if the team has got any letters yet
                if result is not None:
                    returns = []
                    for let in result:
                        returns.append({"letter":let["Letter"], "building":let["Building"], "questionID":let["QuestionID"]})

                    #Checks if the team has got the final letter and won.
                    won = self.checkComplete(teamID)
                    if won["status"] == '1':
                        response = {'status': '2', 'data': returns, 'room' : won["room"]}
                    else:
                        response = {'status': '1', 'data': returns}

        except Exception as e:
            #Error handling
            print(e)
            response = {'status':'0'}
        finally:
            # Return the result
            return response
            con.close()

    """Check if a team has achieved all of the letters needed.

    :param teamID: The team's unique ID.

    :return:  A JSON array with status and the room once finsished."""
    def checkComplete(self, teamID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = makeRowDictionary
                cur = con.cursor()
                #Find all data on the current team
                cur.execute("SELECT * FROM Teams Inner Join Subjects ON Teams.SubjectID = Subjects.SubjectID WHERE TeamID=?", (teamID,))
                Subject = cur.fetchone()
                building = Subject["Building"]
                #Find how far the team has progressed
                cur.execute("SELECT * FROM Results where TeamID=?", (teamID,))
                results = cur.fetchone()
                numLetters = results["Letters"]
                #Check if the team has completed the letters of the building
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
            #Error handling
            print(e)
            return {'status':'0'}
        finally:
            # Return the result

            con.close()

    """Get the answers for a given team.

    :param answer: The answer given by the team.
    :param questionId: The unique ID for the question.
    :param teamID: The team's unique ID.

    :return:  A JSON array with status and letters achieved."""
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
