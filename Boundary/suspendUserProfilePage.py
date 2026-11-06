
'''
What this code does?
- Handle the HTTP POST request for Suspend/Reactivate User Profile.
- Retrieve and validate the selected User Profile ID.
- Extract and strip the submitted suspension or reactivation action.
- Validate that the action is either suspend or reactivate.
- Pass validated information to the Suspend User Profile Controller.
- Return validation errors and status change results to the frontend.
- Does not communicate directly with the Entity.
'''

from flask import request, jsonify


class SuspendUserProfilePage:

    VALID_ACTIONS = {"suspend", "reactivate"}

    # Store the Suspend User Profile Controller
    def __init__(self, suspend_profile_controller):
        self.controller = suspend_profile_controller

    # Handle the Suspend/Reactivate User Profile POST request
    def post(self, profile_id):

        # Retrieve and validate the selected Profile ID
        validated_profile_id, error = self.get_profile_id(
            profile_id
        )

        # Return Profile ID validation errors
        if error:
            return self.display_validation_error(error)

        # Retrieve and validate the requested status action
        action, error = self.get_status_action()

        # Return action validation errors
        if error:
            return self.display_validation_error(error)

        # Pass validated information to the Controller
        result = self.controller.change_profile_status(
            validated_profile_id,
            action
        )

        # Return the status change result through the Boundary
        return self.display_status_result(result)

    # Retrieve and validate the selected User Profile ID
    def get_profile_id(self, profile_id):

        # Validate that the Profile ID is a positive integer
        if (
            not isinstance(profile_id, int)
            or isinstance(profile_id, bool)
            or profile_id <= 0
        ):
            return None, {
                "success": False,
                "message": "Invalid User Profile ID."
            }

        return profile_id, None

    # Retrieve, strip and validate the requested status action
    def get_status_action(self):

        # Retrieve JSON data from the frontend
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Extract and strip the submitted action
        action = data.get("action", "")

        action = (
            action.strip()
            if isinstance(action, str) else ""
        )

        # Validate the requested action
        if action not in self.VALID_ACTIONS:
            return None, {
                "success": False,
                "message": "Invalid profile status action."
            }

        # Return the validated action
        return action, None

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Prepare the Entity's status change result for the frontend
    def display_status_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]
