
'''
What this code does?
- Display the Update User Account HTML page.
- Retrieve existing account details and available User Profiles.
- Retrieve the username from the URL.
- Receive and clean updated account details.
- Validate required fields, email format, role and profile ID.
- Pass valid details to the Controller.
- Return the account update result.
'''

import re
from flask import request, jsonify, render_template
from flask.views import MethodView


class UpdateUserAccountPage(MethodView):

    VALID_ROLES = {"customer", "designer", "admin", "manager"}

    # Receive references to the Controller objects
    def __init__(
        self,
        update_account_controller,
        view_account_controller,
        view_profile_controller
    ):
        self.update_account_controller = update_account_controller
        self.view_account_controller = view_account_controller
        self.view_profile_controller = view_profile_controller

    # Retrieve and clean the submitted account details
    def get_account_details(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        name = data.get("name", "")
        email = data.get("email", "")
        password = data.get("password", "")
        role = data.get("role", "")
        profile_id = data.get("profile_id", None)

        # Convert an empty selection to an unassigned profile
        if profile_id == "":
            profile_id = None

        return {
            "name": name.strip() if isinstance(name, str) else "",
            "email": email.strip() if isinstance(email, str) else "",
            "password": password if isinstance(password, str) else "",
            "role": role.strip() if isinstance(role, str) else "",
            "profile_id": profile_id
        }

    # Validate submitted account information
    def validate_account_details(self, account_details):
        name = account_details["name"]
        email = account_details["email"]
        role = account_details["role"]
        profile_id = account_details["profile_id"]

        if not name or not email or not role:
            return "Please fill in all required fields."

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "Please enter a valid email address."

        if role not in self.VALID_ROLES:
            return "Please select a valid user type."

        # User Profile is optional but must be a positive integer if supplied
        if profile_id is not None:
            if type(profile_id) is not int or profile_id <= 0:
                return "Please select a valid user profile."

        return None

    # Display the Edit Account form with existing account details
    def get(self, account_id):

        # Validate the selected account ID
        if account_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid user account ID."
            }), 400

        # Retrieve the existing account
        account_result, account_status = (
            self.view_account_controller.get_account_by_id(account_id)
        )

        if not account_result["success"]:
            return jsonify(account_result), account_status

        # Retrieve available User Profiles for assignment
        profiles_result, profiles_status = (
            self.view_profile_controller.get_all_profiles()
        )

        if not profiles_result["success"]:
            return jsonify(profiles_result), profiles_status

        username = request.args.get("username", "User Admin").strip()

        if not username:
            username = "User Admin"

        return render_template(
            "updateUserAccount.html",
            account=account_result["account"],
            profiles=profiles_result["profiles"],
            username=username
        ), 200

    # Process the account update request
    def post(self, account_id):

        # Validate the selected account ID
        if account_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid user account ID."
            }), 400

        account_details = self.get_account_details()

        error = self.validate_account_details(account_details)

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        # Pass the validated details to the Controller
        result, status_code = self.update_account_controller.update_account(
            account_id,
            account_details
        )

        return jsonify(result), status_code
