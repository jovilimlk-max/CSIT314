
'''
What this code does?
- Handle Customer Save and Unsave IDP requests.
- Retrieve and validate Customer and Project IDs.
- Pass validated information to the Controller.
- Check whether a Customer has already saved an IDP.
- Return JSON success and error messages to the frontend.
'''

from flask import request, jsonify


class CustomerSaveProjectPage:

    def __init__(self, customer_save_project_controller):
        self.controller = customer_save_project_controller

    # Retrieve and validate the Customer and Project IDs
    def get_save_details(self, project_id):

        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        project_id = str(project_id).strip()

        # Check required IDs
        if not account_id or not project_id:
            return None, {
                "success": False,
                "message": "Customer ID and Project ID are required."
            }

        # Check that both IDs are positive integers
        try:
            account_id = int(account_id)
            project_id = int(project_id)

        except ValueError:
            return None, {
                "success": False,
                "message": "Invalid Customer ID or Project ID."
            }

        if account_id <= 0 or project_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid Customer ID or Project ID."
            }

        return {
            "account_id": account_id,
            "project_id": project_id
        }, None

    # Handle the request to save an IDP
    def post(self, project_id):

        save_details, error = self.get_save_details(project_id)

        if error:
            return self.display_error(error, 400)

        # Save through the Controller
        result, status_code = self.controller.save_project(
            save_details
        )

        return self.display_result(result, status_code)

    # Handle the request to unsave an IDP
    def delete(self, project_id):

        save_details, error = self.get_save_details(project_id)

        if error:
            return self.display_error(error, 400)

        # Remove the saved project through the Controller
        result, status_code = self.controller.unsave_project(
            save_details
        )

        return self.display_result(result, status_code)

    # Handle the request to check saved status
    def get(self, project_id):

        save_details, error = self.get_save_details(project_id)

        if error:
            return self.display_error(error, 400)

        # Check saved status through the Controller
        saved = self.controller.is_project_saved(
            save_details["account_id"],
            save_details["project_id"]
        )

        return self.display_result({
            "success": True,
            "project_id": save_details["project_id"],
            "saved": saved
        }, 200)

    # Return JSON responses
    def display_result(self, result, status_code):

        return jsonify(result), status_code

    # Return validation errors
    def display_error(self, error, status_code):

        return jsonify(error), status_code
