
'''
What this code does?
- Handle requests to suspend or reactivate company information.
- Retrieve the Interior Designer account ID from the URL.
- Receive the requested company status as JSON.
- Validate the account ID and requested status.
- Pass the request to SuspendCompanyInformationController.
- Return the result to the frontend.
'''

from flask import request, jsonify
from flask.views import MethodView


class SuspendCompanyInformationPage(MethodView):

    # Store a reference to the Controller
    def __init__(self, suspend_company_controller):
        self.suspend_company_controller = suspend_company_controller

    # Receive and validate the requested company status
    def get_status_details(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        account_id = request.args.get(
            "account_id",
            type=int
        )

        status = data.get("status", "")

        if not isinstance(status, str):
            status = ""

        return account_id, status.strip()

    # Handle company suspension or reactivation
    def post(self):

        account_id, status = self.get_status_details()

        # Validate the account ID
        if account_id is None or account_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid account ID."
            }), 400

        # Validate the requested status
        if status not in ["active", "suspended"]:
            return jsonify({
                "success": False,
                "message": "Invalid company status."
            }), 400

        # Ask the Controller to change the company status
        result, status_code = (
            self.suspend_company_controller.update_company_status(
                account_id,
                status
            )
        )

        return jsonify(result), status_code
