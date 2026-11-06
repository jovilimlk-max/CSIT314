
'''
What this code does?
- Receive the validated Profile ID from the Update User Profile Boundary.
- Retrieve existing profile information through the User Profile Entity.
- Receive validated updated profile information from the Boundary.
- Pass updated profile information to the Entity.
- Return Entity results to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class UpdateUserProfileController:

    # Store the User Profile Entity
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Retrieve existing profile information for the update form
    def view_user_profile(self, profile_id):

        # Pass the validated Profile ID to the Entity
        result, status_code = self.user_profile.view_profile(
            profile_id
        )

        # Return the Entity result to the calling Boundary
        return result, status_code

    # Coordinate updating an existing User Profile
    def update_user_profile(self, profile_id, profile_details):

        # Pass the validated Profile ID and updated details to the Entity
        result = self.user_profile.update_profile(
            profile_id,
            profile_details
        )

        # Return the Entity result to the calling Boundary
        return result
