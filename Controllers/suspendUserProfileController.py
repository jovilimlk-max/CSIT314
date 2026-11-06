
'''
What this code does?
- Receive the validated Profile ID and status action from the Suspend User Profile Boundary.
- Pass the validated Profile ID and action to the User Profile Entity.
- Return the Entity result to the Boundary.
- Support suspension and reactivation of User Profiles.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class SuspendUserProfileController:

    # Store the User Profile Entity
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Coordinate suspension or reactivation of a User Profile
    def change_profile_status(self, profile_id, action):

        # Pass the validated Profile ID and action to the Entity
        result = self.user_profile.change_profile_status(
            profile_id,
            action
        )

        # Return the Entity result to the calling Boundary
        return result
