
'''
What this code does?
- Check whether the selected User Profile exists.
- Validate the requested suspension or reactivation action.
- Prevent repeated suspension or reactivation.
- Ask the UserProfile Entity to update the profile status.
- Return the suspension or reactivation result.
'''


class SuspendUserProfileController:

    # Store a reference to the UserProfile Entity
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Suspend or reactivate an existing User Profile
    def change_profile_status(self, profile_id, action):

        # Check whether the selected profile exists
        existing_profile = self.user_profile.get_profile_by_id(profile_id)

        if existing_profile is None:
            return {
                "success": False,
                "message": "User Profile not found."
            }, 404

        # Validate the requested action
        if action not in {"suspend", "reactivate"}:
            return {
                "success": False,
                "message": "Invalid profile status action."
            }, 400

        current_status = existing_profile["status"]

        # Determine the new profile status
        if action == "suspend":
            new_status = "suspended"

            if current_status == "suspended":
                return {
                    "success": False,
                    "message": "User Profile is already suspended."
                }, 409

        else:
            new_status = "active"

            if current_status == "active":
                return {
                    "success": False,
                    "message": "User Profile is already active."
                }, 409

        # Ask the Entity to update the profile status
        updated = self.user_profile.update_profile_status(
            profile_id,
            new_status
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update profile status. Please try again."
            }, 409

        # Return the appropriate success message
        if action == "suspend":
            message = "User Profile suspended successfully."
        else:
            message = "User Profile reactivated successfully."

        return {
            "success": True,
            "message": message,
            "status": new_status
        }, 200
