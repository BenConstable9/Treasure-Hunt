from flask import request, session, redirect
from flask import render_template
from Models.adminModel import adminModel
from Helpers.utility import escapeInput

# Author - Ben Constable
# Modified By - Ravi Gohel
# MVC Controller for handling admin login/signup
class AdminAuthController():

    def __init__(self):
        pass

    """Handle the empty page.

    :return: A redirect or a template. """
    def index(self):
        # Check if logged in
        if not session.get('adminLoggedIn'):
            return render_template('admin.html')
        else:
            return redirect("/admin/game", code=302)

    """Handle the form for the logging on

    :return: A redirect or a template. """
    def adminLogin(self):
        # Get the values from the request
        username = request.form.get('Username')
        givenPassword = request.form.get('Password')

        # Get the response from the model
        response = adminModel.adminLogin(escapeInput(username), escapeInput(givenPassword))

        if response["status"] == "1":
            # Set the session varaibles
            session["adminLoggedIn"] = "True"
            session["keeperID"] = response["ID"]
            session["name"] = response["Name"]

            # Redirect
            return redirect("/admin/game",code=302)
        else:
            #should output the error
            return render_template('admin.html', status=response["status"], message=response["message"])


    """Handle the form for the registering new Admin

    :return: A redirect or a template. """
    def adminRegister(self):
        # Get the values from the form
        name = request.form.get('name')
        username = request.form.get('username')
        givenPassword = request.form.get('password1')
        repeatedPassword = request.form.get('password2')

        # Get the response from the model
        response = adminModel.adminRegister(escapeInput(name),escapeInput(username), escapeInput(givenPassword), escapeInput(repeatedPassword))

        if response["status"] == "1":
            # Redirect
            message = response["message"]
        else:
            #should output the error
            response = {}
        return response


    """Handle the form for the changing the password of an Admin

    :return: The response"""
    def adminChangePassword(self):
        # Get the values from the form
        givenPassword = request.form.get('password1')
        repeatedPassword = request.form.get('password2')
        ID = request.form.get('ID')

        # Get the response from the model
        response = adminModel.adminChangePassword(escapeInput(givenPassword), escapeInput(repeatedPassword), escapeInput(ID))

        if response["status"] == "1":
            # Redirect
            message = response["message"]
        else:
            #should output the error
            response = {}
        return response

    """Allow the gamekeeper to Logout

    :return: The response"""
    def adminLogout(self):
        #Get the response from the model
        response = adminModel.adminLogout()
        return response

adminAuthController=AdminAuthController()
