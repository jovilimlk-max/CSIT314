'''
What this code does?
- Receive the email, password and selected user role from the front end, clean the appropriate inputs and pass them to the Controller.
'''

from flask import request, jsonify, render_template
from flask.views import MethodView

class UserLoginPage(MethodView):

    # Receives and stores a reference to the controller object
    def __init__(self, login_controller):
        self.login_controller = login_controller

    # Retrieves submitted data from loginPortal.html and uses .strip() on the email and role
    def get_login_details(self):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            data = {}

        role = data.get("role", "")
        email = data.get("email", "")
        password = data.get("password", "")

        return {
            "role": role.strip() if isinstance(role, str) else "",
            "email": email.strip() if isinstance(email, str) else "",
            "password": password if isinstance(password, str) else ""
        }

    # Receives the HTTP POST request, calls the Controller and returns its result to the front end.
    def post(self):
        login_details = self.get_login_details()

        result, status_code = self.login_controller.login_user(
            login_details
        )

        return jsonify(result), status_code
    
    # Allows the Boundary to serve the login HTML page when Flask receives a GET request.
    def get(self):
        return render_template("LoginPage.html")

