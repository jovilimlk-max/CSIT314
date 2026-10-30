
'''
What this code does?
- Receive login details from the front end.
- Clean email and role inputs.
- Validate required fields, email format and selected role.
- Pass valid login details to the Controller.
- Return the login result to the front end.
'''

import re
from flask import request, jsonify, render_template
from flask.views import MethodView


class UserLoginPage(MethodView):

    VALID_ROLES = {"customer", "designer", "admin", "manager"}

    # Receives and stores a reference to the Controller object
    def __init__(self, login_controller):
        self.login_controller = login_controller

    # Retrieve and clean the submitted login details
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

    # Validate the submitted login details
    def validate_login_details(self, login_details):
        role = login_details["role"]
        email = login_details["email"]
        password = login_details["password"]

        if role not in self.VALID_ROLES:
            return "Please select a valid user type."

        if not email or not password:
            return "Please enter your email address and password."

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "Please enter a valid email address."

        return None

    # Process the login request
    def post(self):
        login_details = self.get_login_details()

        error = self.validate_login_details(login_details)

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        result, status_code = self.login_controller.login_user(
            login_details
        )

        return jsonify(result), status_code

    # Display the login HTML page
    def get(self):
        return render_template("LoginPage.html")
