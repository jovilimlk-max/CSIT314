
'''
What this code does?
- Handle the HTTP GET request for the User Profiles page.
- Retrieve and prepare the User Admin's display name.
- Call the User Profiles Controller to retrieve all user profiles.
- Receive the User Profile information returned by the Controller.
- Display the User Profiles management HTML page.
- Provide profile information for frontend searching and filtering.
- Return an error if profile information cannot be retrieved.
- Does not communicate directly with the Entity.
'''

from flask import render_template, jsonify, request


class UserProfilesPage:

    # Store the User Profiles Controller
    def __init__(self, user_profiles_controller):
        self.controller = user_profiles_controller

    # Handle the User Profiles GET request
    def get(self):

        # Request all User Profiles through the Controller
        result, status_code = self.controller.view_all_profiles()

        # Display the result through the Boundary
        return self.display_profiles(
            result,
            status_code
        )

    # Retrieve and prepare the administrator's display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="User Admin"
        )

        # Strip whitespace and use the default if empty
        username = username.strip()

        if not username:
            username = "User Admin"

        return username

    # Display the User Profiles management page
    def display_profiles(self, result, status_code):

        # Return an error if profiles could not be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Retrieve the administrator's display name
        username = self.get_username()

        # Render the page with the existing profiles
        return render_template(
            "userProfiles.html",
            profiles=result["profiles"],
            username=username
        ), status_code
