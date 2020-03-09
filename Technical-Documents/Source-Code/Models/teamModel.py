from flask import request,json,session
import sqlite3 as sql

# Author - Ben Constable, Debugged with - Ravi Gohel
# Modified By - Ravi
# MVC Model for handling team related data
class TeamModel():
    def __init__(self):
        pass

    """Handling the registering of the teams.
    :param: teamName - the name submitted in the form
    :param: gamePin - the supplied game Pin

    :return: A JSON array with the status. """
    def registerTeam(self, teamName, gamePin, tutorID):
        # Try the SQL
        try:
            # Open the database
            with sql.connect("Models/treasure.sqlite") as con:
                #map the columns to rows
                con.row_factory = sql.Row
                cur = con.cursor()

                # See if the game pin is valid
                cur.execute("SELECT * FROM Games WHERE GamePin=? AND Active=?", (int(gamePin),1))

                game = cur.fetchone()

                if (game is not None):

                    # See if the team name has already been taken for that game
                    cur.execute("SELECT * FROM Teams WHERE GamePin=? AND TeamName=?", (gamePin,teamName))

                    otherTeam = cur.fetchone()

                    #now check the team name and pin combo by checking the length of the return
                    if (otherTeam is None):
                        subject = game["SubjectID"]
                        message = "Team Registration Unsuccessful - "
                        toBreak = False


                        if (len(teamName) == 0):
                            message = message + " Team Name is empty - "
                            toBreak = True


                        team2 = teamName.replace(" ","")
                        if (team2.isalpha()== False):
                            message = message + " Only Letters and Spaces"
                            toBreak = True

                        if (tutorID == "None"):
                            message = message + "Tutor is empty."
                            toBreak = True

                        if (toBreak == True):
                            response = {'status':'0', 'message':message, 'ID': '0'}
                        else:
                            # Insert the team data
                            cur.execute("INSERT INTO Teams (TeamName,GamePin,SubjectID,TutorID) VALUES (?,?,?,?)",(teamName,gamePin,subject,tutorID) )

                            con.commit()

                            # Get the last id
                            lastID = cur.lastrowid

                            response = {'status':'1', 'message':'Team Registration Successfull', 'ID': lastID, 'subject': subject, 'gamePin': gamePin, 'tutor': tutorID}

                    else:
                        response = {'status':'0', 'message':'Team Registration Unsuccessful - Team Name Already Taken', 'ID': '0'}

                else:
                    response = {'status':'0', 'message':'Team Registration Unsuccessful - Game Pin Invalid', 'ID': '0'}

        except Exception as e:
            print(e)
            con.rollback()

            response = {'status':'0', 'message':'Team Registration Unsuccessful - Check All Values', 'ID': '0'}

        finally:
            return response

            con.close()

    """Handling the logging in of the teams.
    :param: teamName - the name submitted in the form
    :param: gamePin - the supplied game Pin

    :return: A JSON array with the status. """
    def loginTeam(self, teamName, gamePin):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                # Get the team name
                cur.execute("SELECT * FROM Teams WHERE GamePin=? AND TeamName=?", (gamePin,teamName))

                team = cur.fetchone()

                # Check the game pin
                if (team is not None):
                    # Formulate the response
                    response = {'status':'1', 'message':'Team Logged In Successfully', 'ID': team["TeamID"], 'subject': team["SubjectID"], 'gamePin': team["GamePin"]}

                else:
                    response = {'status':'0', 'message':'Team Logging In Unsuccessful - Invalid Game Pin', 'ID': '0'}


        except:
            response = {'status':'0', 'message':'Team Logging In Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

    """Handing the logging out of an team"""
    def teamLogout(self):
        session.clear() #Clears the session
        response = {'status':'1', 'message':'Logged Out Successfully'}
        return response

teamModel=TeamModel()
