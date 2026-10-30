
'''
What this code does?
- Display the Create User Profile HTML page.
- Retrieve the administrator's display name from the URL.
- Receive new user profile details.
- Clean the submitted inputs.
- Validate that all required fields are filled in.
- Pass valid profile details to the Controller.
- Return the profile creation result.
'''

from flask import request, jsonify, render_template
from flask.views import MethodView


class CreateUserProfilePage(MethodView):

    # Receive and store a reference to the Controller
    def __init__(self, create_profile_controller):
        self.create_profile_controller = create_profile_controller

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

    # Display the Create User Profile HTML page
    def get(self):
        # Retrieve the administrator's display name
        username = request.args.get(
            "username", "User Admin"
        ).strip()

        if not username:
            username = "User Admin"

        return render_template(
            "createUserProfile.html",
            username=username
        )

    # Process the profile creation request
    def post(self):
        profile_details = self.get_profile_details()

        error = self.validate_profile_details(profile_details)

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        result, status_code = self.create_profile_controller.create_profile(
            profile_details
        )

        return jsonify(result), status_code
