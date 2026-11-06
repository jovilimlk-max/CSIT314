
'''
What this code does?
- Retrieve and prepare the administrator's display name.
- Receive User Profile listing results from the Controller.
- Display the User Profiles management HTML page.
- Provide profile information for frontend searching and filtering.
- Return an error if profile information cannot be retrieved.
'''

from flask import render_template, jsonify, request


class UserProfilesPage:

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
