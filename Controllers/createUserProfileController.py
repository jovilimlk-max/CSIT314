
'''
What this code does?
- Receive validated User Profile information from the Create User Profile Boundary.
- Pass the validated profile information to the User Profile Entity.
- Return the Entity result to the Boundary.
- Does not handle HTTP requests, input validation, HTML or database operations.
'''


class CreateUserProfileController:

    # Store the User Profile Entity
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Coordinate the creation of a new User Profile
    def create_user_profile(self, profile_details):

        # Pass validated profile information to the Entity
        result = self.user_profile.create_profile(
            profile_details
        )

        # Return the Entity result to the calling Boundary
        return result
