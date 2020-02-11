from flask import request,json
import sqlite3 as sql

# Author - Adam Bannister
# MVC Model for handling leaderboard

class leaderboardModel():
    def __init__(self):
        pass

    def obtainResults(self):
        #try the sql
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                # Get the appropriate results
