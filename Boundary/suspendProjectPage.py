
'''
What this code does?
- Retrieve and validate the Interior Designer's Account ID.
- Retrieve and validate the selected Project ID.
- Extract the requested project status from JSON.
- Validate that the requested status is 'active' or 'suspended'.
- Return validation errors as JSON responses.
- Return successful or unsuccessful status updates as JSON.
- Support suspending and reactivating Current IDP and Past IDP.
- Does not directly communicate with Controllers or Entities.
'''

from flask import request, jsonify


class SuspendProjectPage:

    # Retrieve and validate the Interior Designer's Account ID
    def get_account_id(self):

        # Retrieve Account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Check that Account ID is a positive integer
        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        return account_id, None

    # Retrieve and validate the selected Project ID
    def get_project_id(self, project_id):

        # Check that Project ID is a positive integer
        if (
            not isinstance(project_id, int)
            or isinstance(project_id, bool)
            or project_id <= 0
        ):
            return None, {
                "success": False,
                "message": "Invalid project ID."
            }

        return project_id, None

    # Retrieve and validate the requested project status
    def get_requested_status(self):

        # Retrieve submitted JSON data
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Retrieve the requested status
        status = data.get("status", "")

        # Remove unnecessary whitespace
        if isinstance(status, str):
            status = status.strip()

        # Only lowercase active and suspended are accepted
        if status not in ("active", "suspended"):
            return None, {
                "success": False,
                "message": "Invalid project status."
            }

        return status, None

    # Retrieve validated details for changing project status
    def get_status_details(self, project_id):

        # Validate Account ID
        account_id, account_error = self.get_account_id()

        if account_error:
            return None, account_error

        # Validate Project ID
        validated_project_id, project_error = self.get_project_id(
            project_id
        )

        if project_error:
            return None, project_error

        # Validate the requested project status
        status, status_error = self.get_requested_status()

        if status_error:
            return None, status_error

        # Return validated details to the Controller
        return {
            "account_id": account_id,
            "project_id": validated_project_id,
            "status": status
        }, None

    # Return input validation errors
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Return the Entity's status update result
    def display_status_result(self, result, status_code):

        return jsonify(result), status_code
