
'''
What this code does?
- Retrieve the selected User Profile ID from the URL.
- Validate the Profile ID.
- Retrieve and prepare the administrator's display name.
- Display the View User Profile HTML page.
- Return an error if the profile cannot be retrieved.
'''

from flask import render_template, jsonify, request


class ViewUserProfilePage:

    # Retrieve and validate the selected Profile ID
    def get_profile_id(self, profile_id):

        # Validate that the Profile ID is a positive integer
        if not isinstance(profile_id, int) or profile_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid user profile ID."
            }

        return profile_id, None

    # Retrieve and prepare the administrator's display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="User Admin"
        )

        # Strip whitespace and use a default if empty
        username = username.strip()

        if not username:
            username = "User Admin"

        return username

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):
        return jsonify(error), 400

    # Display the selected User Profile
    def display_profile(self, result, status_code):

        # Return an error if the profile could not be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Retrieve the prepared username
        username = self.get_username()

        # Render the View User Profile page
        return render_template(
            "viewUserProfile.html",
            profile=result["profile"],
            username=username
        ), status_code
