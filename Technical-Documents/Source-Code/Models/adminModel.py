from flask import request,json,session
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
    :param: password - the given password
    :param: password2 - the repeated password

    :return: A JSON array with the status. """
    def adminRegister(self, name, username, password1, password2):
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
                    print ("LEN: ", len(otherKeepers))

                    if password1 != password2:
                        response = {'status':'0', 'message':'Game Keeper Registration Unsuccessful - Password Do Not Match', 'ID': '0'}
                    else:
                        salt = os.urandom(32) #Generates the salt

                        # Hash the password
                        storedPassword = hashlib.pbkdf2_hmac(
                            'sha256',
                            password1.encode('utf-8'),
                            salt,
                            100000,
                            dklen=128
                        )

                        # Insert the team data
                        cur.execute("INSERT INTO Keepers (Name,Username,Password,Salt) VALUES (?,?,?,?)",(name,username,storedPassword,salt) )

                        con.commit()

                        # Get the last id
                        lastID = cur.lastrowid

                        response = {'status':'1', 'message':'Game Keeper Registration Successful', 'ID': lastID}

                else:
                    response = {'status':'0', 'message':'Game Keeper Registration Unsuccessful - Username Already Taken', 'ID': '0'}

        except:
            # If a fail then rollback the transaction

            con.rollback()

            response = {'status':'0', 'message':'Game Keeper Registration Unsuccessful', 'ID': '0'}

        finally:
            print (response)
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

                # Check the game pin
                if (givenPassword == keeper["Password"]):

                    # Formulate the response
                    response = {'status':'1', 'message':'Game Keeper Logged In Successfully', 'ID': keeper["KeeperID"], 'Name':keeper["Name"]}

                else:
                    response = {'status':'0', 'message':'Game Keeper Logging In Unsuccessful - Invalid Username or Password', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'Game Keeper Logging In Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            return response

            con.close()



    """Handling the changing of password of an admin.
    :param: password - the given password.
    :param: password2 - the repeated password.
    :param: ID - the ID of the keeper trying to change their password.

    :return: A JSON array with the status. """
    def adminChangePassword(self, password1, password2, ID):
        # Try the SQL
        try:
            # Open the database
            with sql.connect("Models/treasure.sqlite") as con:
                cur = con.cursor()

                if password1 != password2:
                    response = {'status':'0', 'message':'Game Keeper Password Change Unsuccessful - Password Do Not Match'}
                elif len(password1 or password2) == 0:
                    response = {'status':'0', 'message':'Game Keeper Password Change Unsuccessful - Empty password input'}
                else:
                    salt = os.urandom(32) #Generates the salt

                    # Hash the password
                    storedPassword = hashlib.pbkdf2_hmac(
                        'sha256',
                        password1.encode('utf-8'),
                        salt,
                        100000,
                        dklen=128
                    )

                    passwordUpdate = """Update Keepers set Password = ?, Salt = ? where KeeperID = ?"""
                    data = (storedPassword, salt, ID)
                    con.execute(passwordUpdate, data)

                    con.commit()

                    response = {'status':'1', 'message':'Game Keeper Password Changed Successfully'}

        except:
            # If a fail then rollback the transaction

            con.rollback()

            response = {'status':'0', 'message':'Game Keeper Password Change Unsuccessful'}

        finally:
            return response

            con.close()


    """Handing the logging out of an admin"""
    def adminLogout(self):
        session.clear() #Clears the session
        response = {'status':'1', 'message':'Logged Out Successfully'}
        return response



adminModel=AdminModel()
