
'''
What this code does?
- Handle requests to suspend or reactivate a project.
- Retrieve the account ID and Project ID.
- Receive the requested project status.
- Pass the request to SuspendProjectController.
- Return the result as a JSON response.
'''

from flask import request, jsonify
from flask.views import MethodView


class SuspendProjectPage(MethodView):

    # Store a reference to the Controller
    def __init__(self, suspend_project_controller):
        self.suspend_project_controller = suspend_project_controller

    # Handle project suspension or reactivation
    def post(self, project_id):

        # Retrieve the Interior Designer's account ID
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Validate the account ID
        if account_id is None or account_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid account ID."
            }), 400

        # Retrieve the requested status
        data = request.get_json(silent=True) or {}

        status = data.get("status")

        # Ask the Controller to change the project's status
        result, status_code = (
            self.suspend_project_controller.change_project_status(
                account_id,
                project_id,
                status
            )
        )

        # Return the Controller's result
        return jsonify(result), status_code
