
'''
What this code does?
- Coordinate communication between the Suspend User Profile Boundary and Entity.
- Retrieve the validated Profile ID from the Boundary.
- Retrieve the validated suspension or reactivation action from the Boundary.
- Pass the validated information to the Entity.
- Return the Entity result through the Boundary.
- Does not perform business validation or database operations.
'''

from flask.views import MethodView


class SuspendUserProfileController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, suspend_profile_boundary, user_profile):
        self.boundary = suspend_profile_boundary
        self.user_profile = user_profile

    # Coordinate suspension or reactivation of a User Profile
    def post(self, profile_id):

        # Retrieve the validated Profile ID from the Boundary
        validated_id, error = self.boundary.get_profile_id(profile_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Retrieve the validated action from the Boundary
        action, error = self.boundary.get_status_action()

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Pass the validated ID and action to the Entity
        result = self.user_profile.change_profile_status(
            validated_id,
            action
        )

        # Pass the Entity result to the Boundary
        return self.boundary.display_status_result(result)
