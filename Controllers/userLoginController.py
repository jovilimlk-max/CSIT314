
'''
What this code does?
- Ask the UserAccount Entity to authenticate the user.
- Check whether the selected role matches the registered role.
- Check whether the individual account is active.
- Check whether the assigned User Profile is active.
- Return the login result to the Boundary.
'''


class UserLoginController:

    # Store references to the UserAccount and UserProfile Entities
    def __init__(self, user_account, user_profile):
        self.user_account = user_account
        self.user_profile = user_profile

    # Check whether the selected role matches the registered role
    def validate_user_role(self, selected_role, user):
        return selected_role == user.get("role")

    # Check whether the assigned User Profile allows login
    def validate_user_profile(self, profile_id):
        # Accounts without an assigned profile can log in
        if profile_id is None:
            return True

        profile = self.user_profile.get_profile_by_id(profile_id)

        # Do not allow login if the assigned profile does not exist
        if profile is None:
            return False

        return profile["status"] == "active"

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

        # Check the individual account status first
        if user.get("status") != "active":
            return {
                "success": False,
                "message": "Your account has been suspended. Please contact the administrator."
            }, 403

        # Check the assigned User Profile status
        if not self.validate_user_profile(user.get("profile_id")):
            return {
                "success": False,
                "message": "Your assigned user profile is suspended or unavailable. Please contact the administrator."
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
