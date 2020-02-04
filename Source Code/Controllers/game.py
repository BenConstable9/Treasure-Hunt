from flask import request, session, redirect
from flask import render_template

# Author - Ben Constable
# MVC Controller for the game management page
class GameController():

    def __init__(self):
        pass

    """Handle the empty page.

    :return: A redirect or a template. """
    def index(self):
        # Check if logged in
        if not session.get('adminLoggedIn'):
            return redirect("/admin", code=302)
        else:
            return render_template('game.html')

gameController=GameController()
