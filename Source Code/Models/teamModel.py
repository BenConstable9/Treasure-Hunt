from flask import request,json
import sqlite3 as sql

# Author - Ben Constable
# MVC Model for handling team related data
class TeamModel():
    def __init__(self):
        pass

    """Handling the registering of the teams.
    :param: teamName - the name submitted in the form
    :param: gamePin - the supplied game Pin

    :return: A JSON array with the status. """
    def registerTeam(self, teamName, gamePin):
        # Try the SQL
        try:
            # Open the database
            with sql.connect("treasure.db") as con:
                cur = con.cursor()

                # Map the column names
                cur.row_factory = sql.Row

                # See if the game pin is valid
                cur.execute("SELECT * FROM Games WHERE GamePin=? AND Active=1", (gamePin,))

                game = cur.fetchone()

                if (gamePin == game["GamePin"]):

                    # See if the team name has already been taken for that game
                    cur.execute("SELECT * FROM Teams WHERE GamePin=? AND TeamName=1", (gamePin,teamName))

                    otherTeam = cur.fetchall()

                    #now check the team name and pin combo by checking the length of the return
                    if (otherTeam.length == 0):
                        subject = game["Subject"]

                        # Insert the team data
                        cur.execute("INSERT INTO Teams (TeamName,GamePin,Subject) VALUES (?,?,?)",(teamName,gamePin,subject) )

                        con.commit()

                        # Get the last id
                        lastID = cur.lastrowid

                        response = {'status':'1', 'message':'Team Registration Successfull', 'ID': lastID, 'subject': subject, 'gamePin': gamePin}

                    else:
                        response = {'status':'0', 'message':'Team Registration Unsuccessfull - Team Name Already Taken', 'ID': '0'}

                else:
                    response = {'status':'0', 'message':'Team Registration Unsuccessfull - Game Pin Invalid', 'ID': '0'}

        except:
            # If a fail then rollback the transaction

            con.rollback()

            response = {'status':'0', 'message':'Team Registration Unsuccessfull', 'ID': '0'}

        finally:
            return response

            con.close()

    """Handling the registering of the teams.
    :param: teamName - the name submitted in the form
    :param: gamePin - the supplied game Pin

    :return: A JSON array with the status. """
    def loginTeam(self, teamName, gamePin):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("treasure.db") as con:
                cur = con.cursor()
                cur.row_factory = sql.Row

                # Get the team name
                cur.execute("SELECT * FROM Teams WHERE TeamName=?", (teamName,))

                team = cur.fetchone()

                # Check the game pin
                if (gamePin == team["GamePin"]):

                    # Formulate the response
                    response = {'status':'1', 'message':'Team Logged In Successfully', 'ID': team["TeamID"], 'subject': team["Subject"], 'gamePin': team["GamePin"]}

                else:
                    response = {'status':'0', 'message':'Team Logging In Unsuccessfull - Invalid Game Pin', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'Team Logging In Unsuccessfull', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

teamModel=TeamModel()
