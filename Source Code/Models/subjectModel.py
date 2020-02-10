from flask import request,json
import sqlite3 as sql

# Author - Ravi Gohel
# MVC Model for handling user pin

class SubjectModel():
    def __init__(self):
        pass


    """Verifies a pin

    :return: A JSON array with the status. """
    def verifyPin(self, gamePin):
        # Try the SQL
        try:
            # Open the DB
            with sql.connect("Models/treasure.sqlite") as con:
                #map the columns to the rows
                con.row_factory = sql.Row
                cur = con.cursor()

                print ("Gamepin: ", gamePin)

                # cur.execute("INSERT INTO Keepers (Name,Username,Password,Salt) VALUES",('Ravi','Ravi G','1243', 'salt') )
                # con.commit()
                # cur.execute("SELECT * FROM Keepers")
                # print (cur)
                # game = cur.fetchone()
                # print (game)
                #
                # cur.execute("INSERT INTO Subjects (SubjectName,Building,GPS) VALUES (?,?,?)",('Computer Science','Harrison','GPS') )
                # con.commit()
                # cur.execute("SELECT * FROM Subjects")
                # print (cur)
                # game = cur.fetchone()
                # print (game)
                #
                # cur.execute("INSERT INTO Games (SubjectID, GamePin, KeeperID, Active) VALUES (?,?,?,?)",(1,'123',1,1))
                # con.commit()
                # cur.execute("SELECT * FROM Subjects")
                # print (cur)
                # game = cur.fetchone()
                # print (game)
                #
                #
                # game = cur.execute("SELECT * FROM Teams")
                # print (cur)
                # game = cur.fetchone()
                # print (game)

                cur.execute("SELECT * FROM Keepers")
                game = cur.fetchall()
                for row in game:
                    print ("KR1", row[0])
                    print ("KR2", row[1])
                    print ("KR3", row[2])
                    print ("KR4", row[3])
                    print ("KR5", row[4])

                cur.execute("SELECT * FROM Subjects")
                game = cur.fetchall()
                for row in game:
                    print ("SubR1", row[0])
                    print ("SubR2", row[1])
                    print ("SubR3", row[2])
                    print ("SubR4", row[3])

                cur.execute("SELECT * FROM Teams")
                game = cur.fetchall()
                for row in game:
                    print ("T1", row[0])
                    print ("T2", row[1])
                    print ("T3", row[2])
                    print ("T4", row[3])

                cur.execute("SELECT * FROM Games")
                game = cur.fetchall()
                for row in game:
                    print ("TT1", row[0])
                    print ("TT2", row[1])
                    print ("TT3", row[2])
                    print ("TT4", row[3])
                    print ("TT5", row[4])

                #Get the subject associated with that GamePin
                cur.execute ("""
                    SELECT *
                    FROM Subjects
                    INNER JOIN Games
                    ON Subjects.SubjectID = Games.SubjectID
                    WHERE Games.GamePin = ? AND Games.Active='1'""",(gamePin,))
                game = cur.fetchall()
                for row in game:
                    print ("Sub4", row[0])
                    subject = row[0]
                    obtained_row = row



                # # cur.execute("SELECT * FROM Subjects")
                # print ("cur", cur)
                # verified = cur.fetchone()
                #
                # print ("verified", verified)

                # Check the game pin
                if (gamePin == row["GamePin"]):
                    # Formulate the response
                    response = {'status':'1', 'message':'Team Logged In Successfully', 'subjectID': row["SubjectID"], 'subject': row["SubjectName"], 'gamePin': row["GamePin"]}
                    print (response)

                else:
                    response = {'status':'0', 'message':'BAD - Invalid Game Pin', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'BAD - Unsuccessful', 'ID': '0'}

        finally:

            # Return the result
            print ("response: ", response)
            return response

            con.close()

subjectModel=SubjectModel()
