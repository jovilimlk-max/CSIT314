
'''
What this code does?
- Receive the selected user account ID from the URL.
- Validate the account ID.
- Receive the suspension or reactivation action.
- Validate the requested action.
- Pass valid requests to the Controller.
- Return the suspension or reactivation result.
'''

from flask import request, jsonify
from flask.views import MethodView


class SuspendUserAccountPage(MethodView):

    VALID_ACTIONS = {"suspend", "reactivate"}

    # Receive and store a reference to the Controller object
    def __init__(self, suspend_account_controller):
        self.suspend_account_controller = suspend_account_controller

    # Retrieve the submitted suspension or reactivation action
    def get_status_action(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        action = data.get("action", "")

        return action.strip() if isinstance(action, str) else ""

    # Validate the selected account ID and requested action
    def validate_status_action(self, account_id, action):

        if account_id <= 0:
            return "Invalid user account ID."

        if action not in self.VALID_ACTIONS:
            return "Invalid account status action."

        return None

    # Process the account suspension or reactivation request
    def post(self, account_id):
        action = self.get_status_action()

        error = self.validate_status_action(account_id, action)

        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400

        # Pass the valid request to the Controller
        result, status_code = (
            self.suspend_account_controller.change_account_status(
                account_id,
                action
            )
        )

        return jsonify(result), status_code
