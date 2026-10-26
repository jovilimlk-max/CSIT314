
'''
What this code does?
- Retrieve all existing user profiles.
- Retrieve a specific user profile using its ID.
- Ask the UserProfile Entity to retrieve profile information.
- Return the profile retrieval results.
'''


class ViewUserProfileController:

    # Stores a reference to the Entity object
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Retrieve all user profiles for the management page
    def get_all_profiles(self):
        profiles = self.user_profile.get_all_profiles()

        return {
            "success": True,
            "profiles": profiles
        }, 200

    # Retrieve the details of a selected user profile
    def get_profile_by_id(self, profile_id):
        profile = self.user_profile.get_profile_by_id(profile_id)

        if profile is None:
            return {
                "success": False,
                "message": "User profile not found."
            }, 404

        return {
            "success": True,
            "profile": profile
        }, 200
