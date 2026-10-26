
'''
What this code does?
- Check whether the user profile exists.
- Check whether the updated profile name is already in use.
- Ask the Entity to update the user profile.
- Return the profile update result.
'''


class UpdateUserProfileController:

    # Stores a reference to the Entity object
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Coordinate the updating of an existing user profile
    def update_profile(self, profile_id, profile_details):
        profile_name = profile_details["profile_name"]
        description = profile_details["description"]

        # Check whether the selected profile exists
        existing_profile = self.user_profile.get_profile_by_id(profile_id)

        if existing_profile is None:
            return {
                "success": False,
                "message": "User profile not found."
            }, 404

        # Check whether another profile already uses the updated name
        if self.user_profile.profile_name_exists(
            profile_name, exclude_id=profile_id
        ):
            return {
                "success": False,
                "message": "A profile with this name already exists."
            }, 409

        # Ask the Entity to update the profile details
        updated = self.user_profile.update_user_profile(
            profile_id, profile_name, description
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update profile. Please try again."
            }, 409

        return {
            "success": True,
            "message": "User profile updated successfully."
        }, 200
