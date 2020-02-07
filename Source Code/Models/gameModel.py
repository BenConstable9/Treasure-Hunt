from flask import request,json
import sqlite3 as sql
import json

# Author - Ben Constable
# MVC Model for handling admin related data
class GameModel():
    def __init__(self):
        pass

    """Handle the uploading of a game file.

    :param: json - The JSON game file to parsed.

    :return: A JSON object containing the response."""
    def uploadGame(self, json):
        try:
            with open(json) as file:
                contents = json.load(file)

                print(contents)

                response = {'status':'0', 'message':'Subject added successfully.', 'ID': '0'}

        except:
            response = {'status':'0', 'message':'Unable to read in JSON file.', 'ID': '0'}

        finally:
            file.close()

            return response

gameModel=GameModel()
