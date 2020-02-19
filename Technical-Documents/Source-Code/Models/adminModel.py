from flask import request,json
import sqlite3 as sql
import os
import hashlib

# Author - Ben Constable
# Modified - Ravi Gohel
# MVC Model for handling admin related data
class AdminModel():
    def __init__(self):
        pass

    """Handling the registering of the admins.
    :param: name - the name submitted in the form
    :param: username - the username submitted in the form
    :param: password - the supplied game Pin

    :return: A JSON array with the status. """
    def adminRegister(self, name, username, password):
        # Try the SQL
        try:
            # Open the database
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                # See if the username exists
                cur.execute("SELECT * FROM Keepers WHERE Username=?", (username,))

                otherKeepers = cur.fetchall()

                #now check the username is not already taken
                if (len(otherKeepers) == 0):

                    salt = os.urandom(32) #Generates the salt

                    # Hash the password
                    storedPassword = hashlib.pbkdf2_hmac(
                        'sha256',
                        password.encode('utf-8'),
                        salt,
                        100000,
                        dklen=128
                    )

                    # Insert the team data
                    cur.execute("INSERT INTO Keepers (Name,Username,Password,Salt) VALUES (?,?,?,?)",(name,username,storedPassword,salt) )

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

    """Handling the logging in of admins.
    :param: username - the username given in the form
    :param: givenPassword - the supplied password

    :return: A JSON array with the status. """
    def adminLogin(self, username, givenPassword):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                # Get the team name
                cur.execute("SELECT * FROM Keepers WHERE Username=?", (username,))

                keeper = cur.fetchone()

                givenPassword = hashlib.pbkdf2_hmac(
                    'sha256',
                    givenPassword.encode('utf-8'), # Convert the password to bytes
                    keeper["Salt"],
                    100000,
                    dklen=128
                )

                print(givenPassword)

                # Check the game pin
                if (givenPassword == keeper["Password"]):

                    # Formulate the response
                    response = {'status':'1', 'message':'Game Keeper Logged In Successfully', 'ID': keeper["KeeperID"]}

                else:
                    response = {'status':'0', 'message':'Game Keeper Logging In Unsuccessfull - Invalid Username or Password', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'Game Keeper Logging In Unsuccessfull', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()

adminModel=AdminModel()
