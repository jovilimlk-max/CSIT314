
'''
What this code does?
- Handle the HTTP POST request for Create User Profile.
- Display the Create User Profile HTML page.
- Retrieve and prepare the User Admin's display name.
- Extract and strip submitted User Profile information.
- Validate required profile name and description fields.
- Pass validated profile details to the Create User Profile Controller.
- Receive profile creation results from the Controller.
- Return validation errors and creation results to the frontend.
- Does not communicate directly with the Entity.
'''

from flask import request, jsonify, render_template


class CreateUserProfilePage:

    # Store the Create User Profile Controller
    def __init__(self, create_profile_controller):
        self.controller = create_profile_controller

    # Handle the Create User Profile POST request
    def post(self):

        # Retrieve and validate submitted profile information
        profile_details, error = self.get_profile_details()

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass validated profile information to the Controller
        result = self.controller.create_user_profile(
            profile_details
        )

        # Return the creation result through the Boundary
        return self.display_create_profile_result(result)

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

    # Display the Create User Profile HTML page
    def display_create_profile_page(self):

        username = self.get_username()

        return render_template(
            "createUserProfile.html",
            username=username
        )

    # Retrieve, clean and validate submitted profile information
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
        profile_details = {
            "profile_name": profile_name,
            "description": description
        }

        return profile_details, None

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Prepare the profile creation result for the frontend
    def display_create_profile_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]
