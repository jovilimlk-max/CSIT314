
'''
What this code does?
- Extract login details from the frontend.
- Strip email and role inputs without stripping the password.
- Validate required fields, email format and selected role.
- Return validated login details or a validation error.
- Prepare login results for the frontend.
- Display the login HTML page.
'''

import re
from flask import request, jsonify, render_template


class UserLoginPage:

    # Define the available login roles
    VALID_ROLES = {"customer", "designer", "admin", "manager"}

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

    # Prepare the Entity's login result for the frontend
    def display_login_result(self, result):
        return jsonify(result["data"]), result["status_code"]

    # Display the login HTML page
    def display_login_page(self):
        return render_template("LoginPage.html")
