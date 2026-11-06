
'''
What this code does?
- Handle the HTTP GET request for View User Profile.
- Retrieve and validate the selected User Profile ID.
- Retrieve and prepare the administrator's display name.
- Pass the validated Profile ID to the View User Profile Controller.
- Receive the selected profile information from the Controller.
- Display the View User Profile HTML page.
- Return validation and profile retrieval errors.
- Does not communicate directly with the Entity.
'''

from flask import render_template, jsonify, request


class ViewUserProfilePage:

    # Store the View User Profile Controller
    def __init__(self, view_profile_controller):
        self.controller = view_profile_controller

    # Handle the View User Profile GET request
    def get(self, profile_id):

        # Retrieve and validate the selected Profile ID
        validated_profile_id, error = self.get_profile_id(
            profile_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass the validated Profile ID to the Controller
        result, status_code = self.controller.view_user_profile(
            validated_profile_id
        )

        # Display the result through the Boundary
        return self.display_profile(
            result,
            status_code
        )

    # Retrieve and validate the selected Profile ID
    def get_profile_id(self, profile_id):

        # Validate that the Profile ID is a positive integer
        if (
            not isinstance(profile_id, int)
            or isinstance(profile_id, bool)
            or profile_id <= 0
        ):
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
