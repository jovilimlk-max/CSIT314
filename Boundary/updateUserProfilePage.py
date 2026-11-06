
'''
What this code does?
- Retrieve and validate the selected User Profile ID.
- Retrieve the administrator's display name from the URL.
- Extract, strip and validate updated profile information.
- Display the Update User Profile HTML page with existing details.
- Return validation errors and profile update results to the frontend.
'''

from flask import request, jsonify, render_template


class UpdateUserProfilePage:

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

        # Strip whitespace and use a default username if empty
        username = username.strip()

        if not username:
            username = "User Admin"

        return username

    # Extract, strip and validate updated profile information
    def get_profile_details(self):

        # Retrieve JSON data from the frontend
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Extract profile information
        profile_name = data.get("profile_name", "")
        description = data.get("description", "")

        # Strip whitespace from the submitted fields
        profile_name = (
            profile_name.strip()
            if isinstance(profile_name, str) else ""
        )

        description = (
            description.strip()
            if isinstance(description, str) else ""
        )

        # Validate required fields
        if not profile_name or not description:
            return None, {
                "success": False,
                "message": "Please fill in all required fields."
            }

        # Return the validated profile information
        return {
            "profile_name": profile_name,
            "description": description
        }, None

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):
        return jsonify(error), 400

    # Display the Update User Profile page using existing details
    def display_update_profile_page(self, result, status_code):

        # Return an error if the profile could not be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Retrieve the administrator's display name
        username = self.get_username()

        # Render the Update User Profile HTML page
        return render_template(
            "updateUserProfile.html",
            profile=result["profile"],
            username=username
        ), status_code

    # Return the profile update result to the frontend
    def display_update_profile_result(self, result):
        return jsonify(result["data"]), result["status_code"]
