
'''
What this code does?
- Retrieve and validate the selected User Account ID.
- Extract and strip the submitted suspension or reactivation action.
- Validate that the action is either suspend or reactivate.
- Return validated information to the Controller.
- Prepare validation errors and status change results for the frontend.
'''

from flask import request, jsonify


class SuspendUserAccountPage:

    VALID_ACTIONS = {"suspend", "reactivate"}

    # Retrieve and validate the selected Account ID
    def get_account_id(self, account_id):

        # Validate that the Account ID is a positive integer
        if not isinstance(account_id, int) or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid user account ID."
            }

        return account_id, None

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
                "message": "Invalid account status action."
            }

        # Return the validated action
        return action, None

    # Prepare validation errors for the frontend
    def display_validation_error(self, error):
        return jsonify(error), 400

    # Prepare the Entity's status change result for the frontend
    def display_status_result(self, result):
        return jsonify(result["data"]), result["status_code"]
