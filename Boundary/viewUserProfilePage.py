
'''
What this code does?
- Receive the selected user profile ID from the URL.
- Validate the profile ID.
- Request the selected user profile details from the Controller.
- Display the View User Profile HTML page.
- Return an error if the user profile cannot be found.
'''

from flask import render_template, jsonify
from flask.views import MethodView


class ViewUserProfilePage(MethodView):

    # Receives and stores a reference to the Controller object
    def __init__(self, view_profile_controller):
        self.view_profile_controller = view_profile_controller

    # Retrieve and display the selected user profile
    def get(self, profile_id):

        # Validate that the profile ID is a positive integer
        if profile_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid user profile ID."
            }), 400

        # Request the profile details from the Controller
        result, status_code = self.view_profile_controller.get_profile_by_id(
            profile_id
        )

        # Return an error if the profile does not exist
        if not result["success"]:
            return jsonify(result), status_code

        # Display the selected profile information
        return render_template(
            "viewUserProfile.html",
            profile=result["profile"]
        ), status_code
