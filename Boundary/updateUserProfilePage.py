
'''
What this code does?
- Display the Update User Profile HTML page.
- Retrieve the existing user profile details.
- Receive and clean the updated profile details.
- Validate the required fields and profile ID.
- Pass valid details to the Controller.
- Return the profile update result.
'''

from flask import request, jsonify, render_template
from flask.views import MethodView


class UpdateUserProfilePage(MethodView):

    # Receives and stores references to the Controller objects
    def __init__(self, update_profile_controller, view_profile_controller):
        self.update_profile_controller = update_profile_controller
        self.view_profile_controller = view_profile_controller

    # Retrieve and clean the submitted profile details
    def get_profile_details(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        profile_name = data.get("profile_name", "")
        description = data.get("description", "")

        return {
            "profile_name": (
                profile_name.strip()
                if isinstance(profile_name, str) else ""
            ),
            "description": (
                description.strip()
                if isinstance(description, str) else ""
            )
        }

    # Validate the submitted profile details
    def validate_profile_details(self, profile_details):
        profile_name = profile_details["profile_name"]
        description = profile_details["description"]

        if not profile_name or not description:
            return "Please fill in all required fields."

        return None

    # Display the Update User Profile page with existing details
    def get(self, profile_id):

        # Validate the selected profile ID
        if profile_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid user profile ID."
            }), 400

        # Retrieve the existing profile details
        result, status_code = self.view_profile_controller.get_profile_by_id(
            profile_id
        )

        if not result["success"]:
            return jsonify(result), status_code

        return render_template(
            "updateUserProfile.html",
            profile=result["profile"]
        ), status_code

    # Process the profile update request
    def post(self, profile_id):

        # Validate the selected profile ID
        if profile_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid user profile ID."
            }), 400

        profile_details = self.get_profile_details()

        error = self.validate_profile_details(profile_details)

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        # Pass the validated details to the Controller
        result, status_code = self.update_profile_controller.update_profile(
            profile_id, profile_details
        )

        return jsonify(result), status_code
