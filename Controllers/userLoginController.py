'''
What this code does?
- Ask the Entity to authenticate the user.
- Check whether the selected user type matches the registered role.
- Check whether the account is active.
- Return the login result to the Boundary.
'''

class UserLoginController:

    # Stores a reference to the Entity object
    def __init__(self, user_account):
        self.user_account = user_account

    # Check whether the selected role matches the registered role
    def validate_user_role(self, selected_role, user):
        return selected_role == user.get("role")

    # Coordinate authentication and return the result
    def login_user(self, login_details):
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
