from flask import request,json
import sqlite3 as sql

# Author - Adam Bannister
# MVC Model for handling leaderboard

class leaderboardModel():
    def __init__(self):
        pass

    def addLetter(self, teamID,gamePin):
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute("SELECT Letters FROM Results WHERE TeamID=?", (int(TeamID))

                row = cur.fetchone()
                if row is not None:
                    numOfLetters = row["Letters"]


                response = {'status': '1'}
        except Exception as e:
            print(e)
            response = {'status':'0'}
        finally:
            # Return the result
            return response

            con.close()

    def obtainResults(self):
        #try the sql
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                # Get the appropriate results
