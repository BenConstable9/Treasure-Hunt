from jinja2 import utils

# Author - Ben Constable
# Helper for some common utilities

"""Handling the registering of the teams.
:param: input - the input to be santized

:return: A santized string. """
def escapeInput(input):
    return str(utils.escape(input))
