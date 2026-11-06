
'''
What this code does?
- Handle the HTTP POST request for Suspend/Reactivate User Account.
- Retrieve and validate the selected User Account ID.
- Extract and strip the submitted suspension or reactivation action.
- Validate that the action is either suspend or reactivate.
- Pass validated information to the Suspend User Account Controller.
- Return validation errors and status change results to the frontend.
- Does not communicate directly with the Entity.
'''

from flask import request, jsonify


class SuspendUserAccountPage:

    VALID_ACTIONS = {"suspend", "reactivate"}

    # Store the Suspend User Account Controller
    def __init__(self, suspend_account_controller):
        self.controller = suspend_account_controller

    # Handle the Suspend/Reactivate User Account POST request
    def post(self, account_id):

        # Retrieve and validate the selected Account ID
        validated_account_id, error = self.get_account_id(
            account_id
        )

        # Return Account ID validation errors
        if error:
            return self.display_validation_error(error)

        # Retrieve and validate the requested status action
        action, error = self.get_status_action()

        # Return action validation errors
        if error:
            return self.display_validation_error(error)

        # Pass validated information to the Controller
        result = self.controller.change_account_status(
            validated_account_id,
            action
        )

        # Return the status change result through the Boundary
        return self.display_status_result(result)

    # Retrieve and validate the selected Account ID
    def get_account_id(self, account_id):

        # Validate that the Account ID is a positive integer
        if (
            not isinstance(account_id, int)
            or isinstance(account_id, bool)
            or account_id <= 0
        ):
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

        return jsonify(
            result["data"]
        ), result["status_code"]
