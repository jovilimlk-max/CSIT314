
'''
What this code does?
- Coordinate communication between the View User Profile Boundary and Entity.
- Retrieve the validated Profile ID from the Boundary.
- Pass the Profile ID to the Entity to retrieve profile information.
- Pass the Entity result to the Boundary for display.
- Does not perform business logic or database operations.
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
        result, status_code = self.user_profile.view_profile(
            validated_id
        )

        # Pass the Entity result to the Boundary for display
        return self.boundary.display_profile(
            result,
            status_code
        )
