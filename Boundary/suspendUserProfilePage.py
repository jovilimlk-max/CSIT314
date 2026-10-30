
'''
What this code does?
- Receive the selected User Profile ID from the URL.
- Validate the profile ID.
- Receive the suspension or reactivation action.
- Validate the requested action.
- Pass valid requests to the Controller.
- Return the suspension or reactivation result.
'''

from flask import request, jsonify
from flask.views import MethodView


class SuspendUserProfilePage(MethodView):

    VALID_ACTIONS = {"suspend", "reactivate"}

    # Receive and store a reference to the Controller
    def __init__(self, suspend_profile_controller):
        self.suspend_profile_controller = suspend_profile_controller

    # Retrieve the submitted suspension or reactivation action
    def get_status_action(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        action = data.get("action", "")

        return action.strip() if isinstance(action, str) else ""

    # Validate the selected profile ID and requested action
    def validate_status_action(self, profile_id, action):

        if profile_id <= 0:
            return "Invalid User Profile ID."

        if action not in self.VALID_ACTIONS:
            return "Invalid profile status action."

        return None

    # Process the profile suspension or reactivation request
    def post(self, profile_id):
        action = self.get_status_action()

        error = self.validate_status_action(profile_id, action)

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        # Pass the valid request to the Controller
        result, status_code = (
            self.suspend_profile_controller.change_profile_status(
                profile_id,
                action
            )
        )

        return jsonify(result), status_code
