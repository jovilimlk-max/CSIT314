
'''
What this code does?
- Coordinate communication between the Update User Profile Boundary and Entity.
- Retrieve and validate the selected Profile ID through the Boundary.
- Retrieve existing profile information from the Entity for display.
- Retrieve validated updated profile information from the Boundary.
- Pass updated information to the Entity.
- Return Entity results through the Boundary.
'''

from flask.views import MethodView


class UpdateUserProfileController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, update_profile_boundary, user_profile):
        self.boundary = update_profile_boundary
        self.user_profile = user_profile

    # Coordinate displaying the Update User Profile page
    def get(self, profile_id):

        # Retrieve the validated Profile ID from the Boundary
        validated_id, error = self.boundary.get_profile_id(profile_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Request existing profile information from the Entity
        result, status_code = self.user_profile.view_profile(validated_id)

        # Pass the result to the Boundary for display
        return self.boundary.display_update_profile_page(
            result,
            status_code
        )

    # Coordinate updating the selected User Profile
    def post(self, profile_id):

        # Retrieve the validated Profile ID from the Boundary
        validated_id, error = self.boundary.get_profile_id(profile_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Retrieve validated updated information from the Boundary
        profile_details, error = self.boundary.get_profile_details()

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Pass the updated information to the Entity
        result = self.user_profile.update_profile(
            validated_id,
            profile_details
        )

        # Pass the Entity result to the Boundary
        return self.boundary.display_update_profile_result(result)
