
'''
What this code does?
- Receive the validated Profile ID from the View User Profile Boundary.
- Pass the validated Profile ID to the User Profile Entity.
- Retrieve the selected User Profile through the Entity.
- Return the Entity result and status code to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class ViewUserProfileController:

    # Store the User Profile Entity
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Coordinate retrieving an individual User Profile
    def view_user_profile(self, profile_id):

        # Pass the validated Profile ID to the Entity
        result, status_code = self.user_profile.view_profile(
            profile_id
        )

        # Return the Entity result to the calling Boundary
        return result, status_code
