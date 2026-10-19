'''
What this code does?
- Check that the selected user type is valid.
- Check that the email and password are provided.
- Validate the email format.
- Ask the entity to authenticate the user.
- Check wheteher the selected user type matches the user's registered role.
- Check whether the account is active.
- Return the login result to the Boundary.
'''

import re

class UserLoginController:

    VALID_ROLES = {"customer", "designer", "admin", "manager"}

    # Stores a reference to the Entity object so the Controller can call it.
    def __init__(self, user_account):
        self.user_account = user_account

    # Validates the selected role, email and password fields.
    def validate_login_details(self, login_details):
        role = login_details.get("role", "")
        email = login_details.get("email", "")
        password = login_details.get("password", "")

        if role not in self.VALID_ROLES:
            return "Please select a valid user type."

        if not email or not password:
            return "Please enter your email address and password."

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "Please enter a valid email address."

        return None

    # Checks whether the selected role matches the registered account role.
    def validate_user_role(self, selected_role, user):
        return selected_role == user.get("role")

    # Coordinates authentication and returns the result.
    def login_user(self, login_details):
        error = self.validate_login_details(login_details)

        if error:
            return {"success": False, "message": error}, 400

        email = login_details["email"]
        password = login_details["password"]
        role = login_details["role"]

        user = self.user_account.authenticate_user(email, password)

        if user is None:
            return {
                "success": False,
                "message": "Invalid email or password."
            }, 401

        if not self.validate_user_role(role, user):
            return {
                "success": False,
                "message": "Invalid login credentials or user type."
            }, 401

        if user.get("status") != "active":
            return {
                "success": False,
                "message": "This account is not active."
            }, 403

        return {
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "role": user["role"]
            }
        }, 200
        
        
