
'''
What this code does?
- Handle the HTTP POST request for user login.
- Extract login details from the frontend.
- Strip email and role inputs without stripping the password.
- Validate required fields, email format and selected role.
- Pass validated login details to the User Login Controller.
- Receive authentication results from the Controller.
- Return login results and validation errors to the frontend.
- Display the existing login HTML page.
- Support all four user roles.
- Does not communicate directly with the Entity.
'''

import re

from flask import request, jsonify, render_template


class UserLoginPage:

    # Define the available login roles
    VALID_ROLES = {"customer", "designer", "admin", "manager"}

    # Store the User Login Controller
    def __init__(self, user_login_controller):
        self.controller = user_login_controller

    # Handle the User Login POST request
    def post(self):

        # Retrieve and validate submitted login details
        login_details, error = self.get_login_details()

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass validated login details to the Controller
        result = self.controller.authenticate_login(
            login_details
        )

        # Return the authentication result through the Boundary
        return self.display_login_result(result)

    # Retrieve, clean and validate the submitted login details
    def get_login_details(self):

        # Retrieve JSON data from the frontend
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Extract login fields
        role = data.get("role", "")
        email = data.get("email", "")
        password = data.get("password", "")

        # Strip role and email but preserve the original password
        role = role.strip() if isinstance(role, str) else ""
        email = email.strip() if isinstance(email, str) else ""
        password = password if isinstance(password, str) else ""

        # Validate the selected role
        if role not in self.VALID_ROLES:
            return None, {
                "success": False,
                "message": "Please select a valid user type."
            }

        # Validate required fields
        if not email or not password:
            return None, {
                "success": False,
                "message": "Please enter your email address and password."
            }

        # Validate email format
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return None, {
                "success": False,
                "message": "Please enter a valid email address."
            }

        # Return validated login information
        login_details = {
            "role": role,
            "email": email,
            "password": password
        }

        return login_details, None

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Prepare the authentication result for the frontend
    def display_login_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]

    # Display the existing login HTML page
    def display_login_page(self):

        return render_template("LoginPage.html")
