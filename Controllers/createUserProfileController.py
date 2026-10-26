
'''
What this code does?
- Check whether the user profile name already exists.
- Ask the Entity to create the user profile.
- Return the profile creation result.
'''


class CreateUserProfileController:

    # Stores a reference to the Entity object
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Coordinate the creation of a new user profile
    def create_profile(self, profile_details):
        profile_name = profile_details["profile_name"]
        description = profile_details["description"]

        # Check whether the profile name already exists
        if self.user_profile.profile_name_exists(profile_name):
            return {
                "success": False,
                "message": "A profile with this name already exists."
            }, 409

        # Ask the Entity to create the profile
        created = self.user_profile.create_user_profile(
            profile_name, description
        )

        if not created:
            return {
                "success": False,
                "message": "Unable to create profile. Please try again."
            }, 409

        return {
            "success": True,
            "message": "User profile created successfully."
        }, 201
