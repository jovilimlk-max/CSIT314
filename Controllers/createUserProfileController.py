
'''
What this code does?
- Coordinate communication between the Create User Profile Boundary and Entity.
- Retrieve validated profile information from the Boundary.
- Pass profile information to the Entity for creation.
- Pass the Entity result to the Boundary for display.
- Does not perform validation or database operations.
'''

from flask.views import MethodView


class CreateUserProfileController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, create_profile_boundary, user_profile):
        self.boundary = create_profile_boundary
        self.user_profile = user_profile

    # Coordinate the creation of a new User Profile
    def post(self):

        # Retrieve validated profile information from the Boundary
        profile_details, error = self.boundary.get_profile_details()

        # Return Boundary validation errors without calling the Entity
        if error:
            return self.boundary.display_validation_error(error)

        # Pass validated profile information to the Entity
        result = self.user_profile.create_profile(profile_details)

        # Pass the Entity result to the Boundary
        return self.boundary.display_create_profile_result(result)
