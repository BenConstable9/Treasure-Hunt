from flask import Flask,request
from Routes.front import front
import secrets
#from routes.back import back
app = Flask(__name__, template_folder='Views')
app.register_blueprint(front)
#app.register_blueprint(back)

app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

if __name__ == '__main__':
    app.run(debug = True)
