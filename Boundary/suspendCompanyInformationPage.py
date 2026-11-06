
'''
What this code does?
- Handle the HTTP POST request for Suspend/Reactivate Company Information.
- Retrieve the Interior Designer's Account ID from the URL.
- Retrieve the requested company status from submitted JSON.
- Strip unnecessary whitespace from the requested status.
- Validate the Account ID and requested company status.
- Pass validated details to the Suspend Company Information Controller.
- Return validation errors and status update results to the frontend.
- Support both suspension and reactivation of company information.
- Does not communicate directly with the Entity.
'''

from flask import request, jsonify


class SuspendCompanyInformationPage:

    # Store the Suspend Company Information Controller
    def __init__(self, suspend_company_controller):
        self.controller = suspend_company_controller

    # Handle the Suspend/Reactivate Company Information POST request
    def post(self):

        # Retrieve and validate the submitted status details
        status_details, error = self.get_status_details()

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass validated details to the Controller
        result = self.controller.change_company_status(
            status_details
        )

        # Return the result through the Boundary
        return self.display_status_result(result)

    # Retrieve and validate the Interior Designer's Account ID
    def get_account_id(self):

        # Retrieve Account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Validate the Account ID
        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        return account_id, None

    # Retrieve and validate the requested company status
    def get_status_details(self):

        # Retrieve submitted JSON data
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Retrieve and validate the Account ID
        account_id, account_error = self.get_account_id()

        if account_error:
            return None, account_error

        # Retrieve the requested company status
        status = data.get("status", "")

        # Ensure the status is a string
        if not isinstance(status, str):
            status = ""

        # Strip unnecessary whitespace
        status = status.strip()

        # Only allow the two supported company statuses
        if status not in ["active", "suspended"]:
            return None, {
                "success": False,
                "message": "Invalid company status."
            }

        # Return validated details to the Controller
        return {
            "account_id": account_id,
            "status": status
        }, None

    # Return validation errors to the frontend
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Return the company status update result to the frontend
    def display_status_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]
