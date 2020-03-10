from flask import Flask,request
from Routes.front import front
from Routes.admin import admin
import secrets
#from routes.back import back
app = Flask(__name__, template_folder='Views', static_folder='Static')
app.register_blueprint(front)
app.register_blueprint(admin)

# Author - Ben Constable
# MVC Entry point for handling the site

# Make a secret key for the sessions
app.config["SECRET_KEY"] = "tSSmSuHrOjcNAsbV"

if __name__ == '__main__':
    app.run(threaded=True, debug = True)
