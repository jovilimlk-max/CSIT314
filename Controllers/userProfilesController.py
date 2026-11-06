
'''
What this code does?
- Receive a request from the User Profiles Boundary.
- Request all User Profiles from the User Profile Entity.
- Return the Entity result and status code to the Boundary.
- Support the existing User Profiles listing.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class UserProfilesController:

    # Store the User Profile Entity
    def __init__(self, user_profile):
        self.user_profile = user_profile

    # Coordinate retrieving all User Profiles
    def view_all_profiles(self):

        # Request all User Profiles from the Entity
        result, status_code = self.user_profile.view_all_profiles()

        # Return the Entity result to the calling Boundary
        return result, status_code
