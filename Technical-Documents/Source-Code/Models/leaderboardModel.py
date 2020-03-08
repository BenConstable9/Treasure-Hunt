from flask import request,json
import sqlite3 as sql

# Author - Adam Bannister
# MVC Model for handling leaderboard

class leaderboardModel():
    def __init__(self):
        pass


    def addLetter(self, teamID):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute("SELECT Letters FROM Results WHERE TeamID=?", (int(teamID)))

                row = cur.fetchone()
                if row is not None:
                    numOfLetters = row["Letters"]
                    numOfLetters +=1
                    cur.execute("UPDATE Results SET Letters =? WHERE TeamID=?", (int(numOfLetters)),(int(teamID)))

                response = {'status': '1'}
        except Exception as e:
            print(e)
            response = {'status':'0'}
        finally:
            # Return the result
            return response

            con.close()

    """Fetch the relevant data for results for the leaderboard

    :param gamePin: the gamePin to create results for

    :return: a json response containing leaderboard data"""

    def obtainResults(self, gamePin):
        #try the sql
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                #map the column names to the values returned
                #con.row_factory = makeRowDictionary
                cur = con.cursor()

                # Get the appropriate results
                cur.execute("SELECT t.TeamName, r.StartTime, r.FinishTime, r.Letters, t.GamePin FROM Teams t INNER JOIN Results r ON t.TeamID = r.TeamID WHERE t.Gamepin=?", (gamePin,))

                results = cur.fetchall()

                response = {'status':'1', 'data':results}
        except Exception as e:
            print(e)
            response = {'status':'0', 'message':'BAD - Unsuccessful'}

        finally:
            print(response)

            # Return the result
            return response

            con.close()

leaderboardModel=leaderboardModel()
