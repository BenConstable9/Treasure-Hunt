from jinja2 import utils

# Author - Ben Constable
# Helper for some common utilities

"""Handling the registering of the teams.

:param: input - the input to be santized

:return: A santized string. """
def escapeInput(input):
    return str(utils.escape(input))

"""Map the column names to the values so it acts as dictionary.

:param cursor: The cursor object

:param row: The row data

:return: A dictionary of values and names. """
def makeRowDictionary(cursor, row):
    #map into a dictionary
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
