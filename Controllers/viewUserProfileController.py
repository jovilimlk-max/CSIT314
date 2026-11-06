
'''
What this code does?
- Coordinate communication between the View User Profile Boundary and Entity.
- Retrieve the validated Profile ID from the Boundary.
- Pass the Profile ID to the Entity to retrieve profile information.
- Pass the Entity result to the Boundary for display.
- Temporarily preserve existing methods used by other features.
'''

from flask.views import MethodView


class ViewUserProfileController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, view_profile_boundary, user_profile):
        self.boundary = view_profile_boundary
        self.user_profile = user_profile

    # Coordinate viewing an individual User Profile
    def get(self, profile_id):

        # Retrieve the validated Profile ID from the Boundary
        validated_id, error = self.boundary.get_profile_id(profile_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Pass the Profile ID to the Entity
        result, status_code = self.user_profile.view_profile(validated_id)

        # Pass the Entity result to the Boundary for display
        return self.boundary.display_profile(
            result,
            status_code
        )

    # Existing method retained for User Profile listing
    # To be refactored when working on the listing feature
    def get_all_profiles(self):
        profiles = self.user_profile.get_all_profiles()

        return {
            "success": True,
            "profiles": profiles
        }, 200

    # Existing method retained for other dependent features
    # To be refactored when those features are updated
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
