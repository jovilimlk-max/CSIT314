
'''
What this code does?
- Check whether the user account exists.
- Check whether the updated email is already in use.
- Check whether the selected user profile exists, if assigned.
- Hash a new password if one is provided.
- Ask the Entity to update the user account.
- Return the account update result.
'''

from werkzeug.security import generate_password_hash


class UpdateUserAccountController:

    # Store references to the UserAccount and UserProfile Entities
    def __init__(self, user_account, user_profile):
        self.user_account = user_account
        self.user_profile = user_profile

    # Coordinate the updating of an existing user account
    def update_account(self, account_id, account_details):
        name = account_details["name"]
        email = account_details["email"]
        password = account_details["password"]
        role = account_details["role"]
        profile_id = account_details["profile_id"]

        # Check whether the selected account exists
        existing_account = self.user_account.get_account_by_id(account_id)

        if existing_account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Check whether another account already uses the updated email
        if self.user_account.email_exists(email, exclude_id=account_id):
            return {
                "success": False,
                "message": "Email address is already registered."
            }, 409

        # Check whether the selected User Profile exists
        if profile_id is not None:
            existing_profile = self.user_profile.get_profile_by_id(profile_id)

            if existing_profile is None:
                return {
                    "success": False,
                    "message": "Selected user profile not found."
                }, 404

        # Only hash the password if a new one was entered
        password_hash = None

        if password:
            password_hash = generate_password_hash(password)

        # Ask the Entity to update the account details
        updated = self.user_account.update_user_account(
            account_id,
            name,
            email,
            role,
            profile_id,
            password_hash
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update account. Please try again."
            }, 409

        return {
            "success": True,
            "message": "User account updated successfully."
        }, 200
