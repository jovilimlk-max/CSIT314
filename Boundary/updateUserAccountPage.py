
'''
What this code does?
- Handle GET and POST requests for Update User Account.
- Retrieve and validate the selected User Account ID.
- Retrieve and prepare the administrator's display name.
- Extract and strip updated account information, except the password.
- Validate required fields, email format, selected role and optional Profile ID.
- Allow password and User Profile assignment to remain optional.
- Call the Update User Account Controller to retrieve existing account details.
- Pass validated updated account information to the Controller.
- Display the Update User Account page with existing account details.
- Return validation errors and account update results to the frontend.
- Does not communicate directly with the Entity.
'''

import re

from flask import request, jsonify, render_template


class UpdateUserAccountPage:

    VALID_ROLES = {"customer", "designer", "admin", "manager"}

    # Store the Update User Account Controller
    def __init__(self, update_account_controller):
        self.controller = update_account_controller

    # Handle the GET request to display the Update User Account page
    def get(self, account_id):

        # Retrieve and validate the selected Account ID
        validated_account_id, error = self.get_account_id(
            account_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Call the Controller to retrieve existing account details
        result, status_code = self.controller.get_account_update_details(
            validated_account_id
        )

        # Display the existing account information
        return self.display_update_account_page(
            result,
            status_code
        )

    # Handle the POST request to update the User Account
    def post(self, account_id):

        # Retrieve and validate the selected Account ID
        validated_account_id, error = self.get_account_id(
            account_id
        )

        # Return Account ID validation errors
        if error:
            return self.display_validation_error(error)

        # Retrieve and validate submitted account information
        account_details, error = self.get_account_details()

        # Return field validation errors
        if error:
            return self.display_validation_error(error)

        # Pass validated details to the Controller
        result = self.controller.update_user_account(
            validated_account_id,
            account_details
        )

        # Return the update result through the Boundary
        return self.display_update_account_result(result)

    # Retrieve and validate the selected Account ID
    def get_account_id(self, account_id):

        # Validate that the Account ID is a positive integer
        if (
            not isinstance(account_id, int)
            or isinstance(account_id, bool)
            or account_id <= 0
        ):
            return None, {
                "success": False,
                "message": "Invalid user account ID."
            }

        return account_id, None

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

    # Retrieve, clean and validate updated account information
    def get_account_details(self):

        # Retrieve JSON data from the frontend
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Extract submitted account information
        name = data.get("name", "")
        email = data.get("email", "")
        password = data.get("password", "")
        role = data.get("role", "")
        profile_id = data.get("profile_id", None)

        # Strip whitespace from all text fields except password
        name = name.strip() if isinstance(name, str) else ""
        email = email.strip() if isinstance(email, str) else ""
        password = password if isinstance(password, str) else ""
        role = role.strip() if isinstance(role, str) else ""

        # Convert an empty profile selection to no assigned profile
        if profile_id == "":
            profile_id = None

        # Validate required fields
        if not name or not email or not role:
            return None, {
                "success": False,
                "message": "Please fill in all required fields."
            }

        # Validate email address format
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return None, {
                "success": False,
                "message": "Please enter a valid email address."
            }

        # Validate selected role
        if role not in self.VALID_ROLES:
            return None, {
                "success": False,
                "message": "Please select a valid user type."
            }

        # Validate optional User Profile ID
        if profile_id is not None:
            if type(profile_id) is not int or profile_id <= 0:
                return None, {
                    "success": False,
                    "message": "Please select a valid user profile."
                }

        # Return validated account information
        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "profile_id": profile_id
        }, None

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Display the Update User Account page
    def display_update_account_page(self, result, status_code):

        # Return an error if account information cannot be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Retrieve the administrator's display name
        username = self.get_username()

        # Render the form with the existing account and available profiles
        return render_template(
            "updateUserAccount.html",
            account=result["account"],
            profiles=result["profiles"],
            username=username
        ), status_code

    # Return the account update result to the frontend
    def display_update_account_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]
