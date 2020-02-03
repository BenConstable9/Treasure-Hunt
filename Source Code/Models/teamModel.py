from flask import request,json
import sqlite3 as sql

class TeamModel():
    def __init__(self):
        pass

    def registerTeam(self, TeamName, Password, Subject):
        #insert them
        try:
            #when are we meant to open it
            with sql.connect("treasure.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO Teams (TeamName,Password,Subject) VALUES (?,?,?)",(TeamName,Password,Subject) )

                con.commit()

                lastID = cur.lastrowid

                response = {'Status':'1', 'Message':'Team Registration Successfull', 'ID': lastID}

        except:
            con.rollback()
            response = {'Status':'0', 'Message':'Team Registration Unsuccessfull', 'ID': '0'}

        finally:
            return response

            con.close()

    def loginTeam(self, teamName, password):
        #insert them
        try:
            #when are we meant to open it
            with sql.connect("treasure.db") as con:
                cur = con.cursor()
                cur.row_factory = sql.Row

                cur.execute("SELECT * FROM Teams WHERE TeamName=?", (teamName,))

                team = cur.fetchone()

                #todo handle hashing
                if (password == team["Password"]):

                    response = {'Status':'1', 'Message':'Team Logged In Successfully', 'ID': team["TeamID"]}

                else:
                    response = {'Status':'0', 'Message':'Team Logging In Unsuccessfull - Invalid Password', 'ID': '0'}

        except:
            response = {'Status':'0', 'Message':'Team Logging In Unsuccessfull', 'ID': '0'}

        finally:
            return response

            con.close()

teamModel=TeamModel()
