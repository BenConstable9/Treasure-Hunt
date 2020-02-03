from flask import request,json
import sqlite3 as sql

# Author - Ben Constable
# MVC Model for handling team related data
class TeamModel():
    def __init__(self):
        pass

    def registerTeam(self, teamName, gamePin):
        #insert them
        try:
            #when are we meant to open it
            with sql.connect("treasure.db") as con:
                cur = con.cursor()

                cur.row_factory = sql.Row

                cur.execute("SELECT * FROM Games WHERE GamePin=? AND Active=1", (gamePin,))

                game = cur.fetchone()

                if (gamePin == game["GamePin"]):

                    cur.execute("SELECT * FROM Teams WHERE GamePin=? AND TeamName=1", (gamePin,teamName))

                    otherTeam = cur.fetchall()

                    #now check the team name and pin combo

                    if (otherTeam.length == 0):
                        subject = game["Subject"]

                        cur.execute("INSERT INTO Teams (TeamName,GamePin,Subject) VALUES (?,?,?)",(teamName,gamePin,subject) )

                        con.commit()

                        lastID = cur.lastrowid

                        response = {'status':'1', 'message':'Team Registration Successfull', 'ID': lastID, 'subject': subject, 'gamePin': gamePin}

                    else:
                        response = {'status':'0', 'message':'Team Registration Unsuccessfull - Team Name Already Taken', 'ID': '0'}

                else:
                    response = {'status':'0', 'message':'Team Registration Unsuccessfull - Game Pin Invalid', 'ID': '0'}

        except:
            con.rollback()
            response = {'status':'0', 'message':'Team Registration Unsuccessfull', 'ID': '0'}

        finally:
            return response

            con.close()

    def loginTeam(self, teamName, gamePin):
        #insert them
        try:
            #when are we meant to open it
            with sql.connect("treasure.db") as con:
                cur = con.cursor()
                cur.row_factory = sql.Row

                cur.execute("SELECT * FROM Teams WHERE TeamName=?", (teamName,))

                team = cur.fetchone()

                #todo handle hashing
                if (gamePin == team["GamePin"]):

                    response = {'status':'1', 'message':'Team Logged In Successfully', 'ID': team["TeamID"], 'subject': team["Subject"], 'gamePin': team["GamePin"]}

                else:
                    response = {'status':'0', 'message':'Team Logging In Unsuccessfull - Invalid Password', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'Team Logging In Unsuccessfull', 'ID': '0'}

        finally:
            return response

            con.close()

teamModel=TeamModel()
