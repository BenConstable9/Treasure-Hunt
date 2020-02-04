from flask import request,json
import sqlite3 as sql
import os
import hashlib

# Author - Ben Constable
# MVC Model for handling admin related data
class TeamModel():
    def __init__(self):
        pass

    """Handling the registering of the admins.
    :param: name - the name submitted in the form
    :param: username - the username submitted in the form
    :param: password - the supplied game Pin

    :return: A JSON array with the status. """
    def registerAdmin(self, name, username, password):
        # Try the SQL
        try:
            # Open the database
            with sql.connect("treasure.db") as con:
                cur = con.cursor()

                # See if the username exists
                cur.execute("SELECT * FROM Keepers WHERE Username=?", (username,))

                otherKeepers = cur.fetchall()

                #now check the username is not already taken
                if (otherKeepers.length == 0):

                    salt = os.urandom(32)

                    # Hash the password
                    storedPassword = hashlib.pbkdf2_hmac(
                        'sha256',
                        password.encode('utf-8'),
                        salt,
                        100000,
                        dklen=128
                    )

                    # Insert the team data
                    cur.execute("INSERT INTO Keepers (Name,Username,Password,Salt) VALUES (?,?,?)",(name,username,storedPassword,salt) )

                    con.commit()

                    # Get the last id
                    lastID = cur.lastrowid

                    response = {'status':'1', 'message':'Game Keeper Registration Successfull', 'ID': lastID}

                else:
                    response = {'status':'0', 'message':'Game Keeper Registration Unsuccessfull - Username Already Taken', 'ID': '0'}

        except:
            # If a fail then rollback the transaction

            con.rollback()

            response = {'status':'0', 'message':'Game Keeper Registration Unsuccessfull', 'ID': '0'}

        finally:
            return response

            con.close()

    """Handling the registering of the teams.
    :param: teamName - the name submitted in the form
    :param: gamePin - the supplied game Pin

    :return: A JSON array with the status. """
    def loginAdmin(self, username, givenPassword):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("treasure.db") as con:
                cur = con.cursor()
                cur.row_factory = sql.Row

                # Get the team name
                cur.execute("SELECT * FROM Keepers WHERE Username=?", (username,))

                admin = cur.fetchone()

                givenPassword = hashlib.pbkdf2_hmac(
                    'sha256',
                    givenPassword.encode('utf-8'), # Convert the password to bytes
                    admin["Salt"],
                    100000
                )

                # Check the game pin
                if (givenPassword == admin["Password"]):

                    # Formulate the response
                    response = {'status':'1', 'message':'Game Keeper Logged In Successfully', 'ID': admin["KeeperID"]}

                else:
                    response = {'status':'0', 'message':'Game Keeper Logging In Unsuccessfull - Invalid Username or Password', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'Game Keeper Logging In Unsuccessfull', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

adminModel=AdminModel()