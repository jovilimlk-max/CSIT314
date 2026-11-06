
'''
What this code does?
- Handle GET and POST requests for Update User Profile.
- Retrieve and validate the selected User Profile ID.
- Retrieve and prepare the administrator's display name.
- Extract and strip updated profile information.
- Validate required profile name and description fields.
- Call the Update User Profile Controller to retrieve existing details.
- Pass validated updated profile information to the Controller.
- Display the Update User Profile page with existing details.
- Return validation errors and profile update results to the frontend.
- Does not communicate directly with the Entity.
'''

from flask import request, jsonify, render_template


class UpdateUserProfilePage:

    # Store the Update User Profile Controller
    def __init__(self, update_profile_controller):
        self.controller = update_profile_controller

    # Handle the GET request to display the Update User Profile page
    def get(self, profile_id):

        # Retrieve and validate the selected Profile ID
        validated_profile_id, error = self.get_profile_id(
            profile_id
        )

        # Return Profile ID validation errors
        if error:
            return self.display_validation_error(error)

        # Call the Controller to retrieve existing profile information
        result, status_code = self.controller.view_user_profile(
            validated_profile_id
        )

        # Display the existing profile details through the Boundary
        return self.display_update_profile_page(
            result,
            status_code
        )

    # Handle the POST request to update a User Profile
    def post(self, profile_id):

        # Retrieve and validate the selected Profile ID
        validated_profile_id, error = self.get_profile_id(
            profile_id
        )

        # Return Profile ID validation errors
        if error:
            return self.display_validation_error(error)

        # Retrieve and validate submitted profile information
        profile_details, error = self.get_profile_details()

        # Return field validation errors
        if error:
            return self.display_validation_error(error)

        # Pass validated information to the Controller
        result = self.controller.update_user_profile(
            validated_profile_id,
            profile_details
        )

        # Return the update result through the Boundary
        return self.display_update_profile_result(result)

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
