
'''
What this code does?
- Handle Suspend and Reactivate IDP Category requests.
- Retrieve the Category ID from the URL.
- Retrieve the requested status from the JSON request.
- Validate the Category ID and requested status.
- Pass validated information to the Suspend IDP Category Controller.
- Return success or error messages as JSON to the frontend.
- Keep HTTP handling and input validation in Boundary.
- Keep database operations and domain checks in Entity.
'''

from flask import request, jsonify


class SuspendIDPCategoryPage:

    # Store the Suspend IDP Category Controller
    def __init__(self, suspend_idp_category_controller):
        self.controller = suspend_idp_category_controller

    # Handle a Suspend or Reactivate request
    def post(self, category_id):

        # Validate the Category ID from the URL
        try:
            category_id = int(category_id)

        except (TypeError, ValueError):
            return self.display_error(
                "Invalid IDP Category ID.",
                400
            )

        if category_id <= 0:
            return self.display_error(
                "Invalid IDP Category ID.",
                400
            )

        # Retrieve JSON information from the confirmation pop-up
        request_data = request.get_json(silent=True)

        if not isinstance(request_data, dict):
            return self.display_error(
                "Invalid request data.",
                400
            )

        # Retrieve and trim the requested status
        new_status = request_data.get("status", "")

        if not isinstance(new_status, str):
            return self.display_error(
                "Invalid category status.",
                400
            )

        new_status = new_status.strip()

        # Validate required status and supported values
        if not new_status:
            return self.display_error(
                "Category status is required.",
                400
            )

        if new_status not in ("active", "suspended"):
            return self.display_error(
                "Invalid category status.",
                400
            )

        # Pass the validated request to the Controller
        result, status_code = self.controller.change_category_status(
            category_id,
            new_status
        )

        # Return the Entity result through the Controller
        return jsonify(result), status_code

    # Return validation errors to the frontend
    def display_error(self, message, status_code):

        return jsonify({
            "success": False,
            "message": message
        }), status_code
