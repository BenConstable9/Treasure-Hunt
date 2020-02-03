from flask import request,json
import sqlite3 as sql

class TeamModel():
    def __init__(self):
        pass

    def getUser(_id):
        users = mongo.db.users.find({'_id': _id})
        x = []
        for user in users:
            x.append(user)
        return user

    def getAllUser(_id):
        users = mongo.db.users.find()
        return toDictionaryArray(users)

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

                print(response)
        except:
            con.rollback()
            response = {'Status':'0', 'Message':'Team Registration Unsuccessfull', 'ID': '0'}

            print(response)

        finally:
            return response

            con.close()

teamModel=TeamModel()
