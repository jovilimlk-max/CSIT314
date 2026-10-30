
'''
What this code does?
- Display the Create User Account HTML page.
- Retrieve the username from the URL.
- Receive new user account details.
- Clean the appropriate inputs.
- Validate required fields, email format and selected role.
- Pass valid account details to the Controller.
- Return the account creation result.
'''

import re
from flask import request, jsonify, render_template
from flask.views import MethodView


class CreateUserAccountPage(MethodView):

    VALID_ROLES = {"customer", "designer", "admin", "manager"}

    # Receives and stores a reference to the Controller object
    def __init__(self, create_account_controller):
        self.create_account_controller = create_account_controller

    # Retrieve and clean the submitted account details
    def get_account_details(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        name = data.get("name", "")
        email = data.get("email", "")
        password = data.get("password", "")
        role = data.get("role", "")

        return {
            "name": name.strip() if isinstance(name, str) else "",
            "email": email.strip() if isinstance(email, str) else "",
            "password": password if isinstance(password, str) else "",
            "role": role.strip() if isinstance(role, str) else ""
        }

    # Validate the submitted account details
    def validate_account_details(self, account_details):
        name = account_details["name"]
        email = account_details["email"]
        password = account_details["password"]
        role = account_details["role"]

        if not name or not email or not password or not role:
            return "Please fill in all required fields."

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "Please enter a valid email address."

        if role not in self.VALID_ROLES:
            return "Please select a valid user type."

        return None

    # Display the Create User Account HTML page
    def get(self):
        username = request.args.get("username", "User Admin").strip()

        if not username:
            username = "User Admin"

        return render_template(
            "createUserAccount.html",
            username=username
        )

    # Process the account creation request
    def post(self):
        account_details = self.get_account_details()

        error = self.validate_account_details(account_details)

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        result, status_code = self.create_account_controller.create_account(
            account_details
        )

        return jsonify(result), status_code
