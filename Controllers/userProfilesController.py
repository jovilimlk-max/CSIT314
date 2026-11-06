
'''
What this code does?
- Coordinate communication between the User Profiles Boundary and Entity.
- Request the list of existing User Profiles from the Entity.
- Pass the Entity result to the Boundary for display.
- Support the existing frontend search and filtering functionality.
- Does not perform validation or database operations.
'''

from flask.views import MethodView


class UserProfilesController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, profiles_boundary, user_profile):
        self.boundary = profiles_boundary
        self.user_profile = user_profile

    # Coordinate retrieving and displaying all User Profiles
    def get(self):

        # Request the complete profile listing from the Entity
        result, status_code = self.user_profile.view_all_profiles()

        # Pass the Entity result to the Boundary for display
        return self.boundary.display_profiles(
            result,
            status_code
        )
