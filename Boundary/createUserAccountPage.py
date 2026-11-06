
'''
What this code does?
- Handle the HTTP POST request for Create User Account.
- Display the Create User Account HTML page.
- Retrieve and prepare the administrator's display name.
- Extract and strip new account information, except the password.
- Validate required fields, email format and selected role.
- Pass validated account details to the Create User Account Controller.
- Receive account creation results from the Controller.
- Return validation errors and creation results to the frontend.
- Does not communicate directly with the Entity.
'''

import re

from flask import request, jsonify, render_template


class CreateUserAccountPage:

    VALID_ROLES = {"customer", "designer", "admin", "manager"}

    # Store the Create User Account Controller
    def __init__(self, create_account_controller):
        self.controller = create_account_controller

    # Handle the Create User Account POST request
    def post(self):

        # Retrieve and validate submitted account information
        account_details, error = self.get_account_details()

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass validated account information to the Controller
        result = self.controller.create_user_account(
            account_details
        )

        # Return the account creation result through the Boundary
        return self.display_create_account_result(result)

    # Retrieve and prepare the administrator's display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="User Admin"
        )

        # Strip whitespace and use a default if empty
        username = username.strip()

        if not username:
            username = "User Admin"

        return username

    # Display the Create User Account HTML page
    def display_create_account_page(self):

        username = self.get_username()

        return render_template(
            "createUserAccount.html",
            username=username
        )

    # Retrieve, clean and validate submitted account information
    def get_account_details(self):

        # Retrieve JSON data from the frontend
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Extract the submitted account information
        name = data.get("name", "")
        email = data.get("email", "")
        password = data.get("password", "")
        role = data.get("role", "")

        # Strip whitespace from all fields except the password
        name = name.strip() if isinstance(name, str) else ""
        email = email.strip() if isinstance(email, str) else ""
        password = password if isinstance(password, str) else ""
        role = role.strip() if isinstance(role, str) else ""

        # Validate all required fields
        if not name or not email or not password or not role:
            return None, {
                "success": False,
                "message": "Please fill in all required fields."
            }

        # Validate the email address format
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return None, {
                "success": False,
                "message": "Please enter a valid email address."
            }

        # Validate the selected role
        if role not in self.VALID_ROLES:
            return None, {
                "success": False,
                "message": "Please select a valid user type."
            }

        # Return validated account information
        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }, None

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Prepare the account creation result for the frontend
    def display_create_account_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]
