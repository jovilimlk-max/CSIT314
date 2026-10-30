
'''
What this code does?
- Check whether the selected user account exists.
- Check whether the requested suspension or reactivation is valid.
- Prevent repeated suspension or reactivation.
- Ask the UserAccount Entity to update the account status.
- Return the suspension or reactivation result.
'''


class SuspendUserAccountController:

    # Store a reference to the UserAccount Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Suspend or reactivate an existing user account
    def change_account_status(self, account_id, action):

        # Check whether the selected account exists
        existing_account = self.user_account.get_account_by_id(account_id)

        if existing_account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Validate the requested action
        if action not in {"suspend", "reactivate"}:
            return {
                "success": False,
                "message": "Invalid account status action."
            }, 400

        current_status = existing_account["status"]

        # Determine the new account status
        if action == "suspend":
            new_status = "suspended"

            if current_status == "suspended":
                return {
                    "success": False,
                    "message": "User account is already suspended."
                }, 409

        else:
            new_status = "active"

            if current_status == "active":
                return {
                    "success": False,
                    "message": "User account is already active."
                }, 409

        # Ask the Entity to update the account status
        updated = self.user_account.update_account_status(
            account_id,
            new_status
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update account status. Please try again."
            }, 409

        # Return the appropriate success message
        if action == "suspend":
            message = "User account suspended successfully."
        else:
            message = "User account reactivated successfully."

        return {
            "success": True,
            "message": message,
            "status": new_status
        }, 200
