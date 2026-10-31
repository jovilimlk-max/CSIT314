
'''
What this code does?
- Display the Create Project page.
- Verify that the Interior Designer has company information.
- Retrieve the account ID and username from the URL.
- Pass project details to CreateProjectController.
- Return the result of project creation.
'''

from flask import request, render_template, jsonify
from flask.views import MethodView


class CreateProjectPage(MethodView):

    # Store references to the Controllers
    def __init__(self, create_project_controller, view_company_controller):
        self.create_project_controller = create_project_controller
        self.view_company_controller = view_company_controller

    # Display the Create Project page
    def get(self):

        account_id = request.args.get(
            "account_id",
            type=int
        )

        username = request.args.get(
            "username",
            default="Interior Designer"
        )

        # Validate the account ID
        if account_id is None or account_id <= 0:
            return "Invalid account ID.", 400

        # Retrieve company information through the existing Controller
        result, status_code = (
            self.view_company_controller.view_company_information(
                account_id
            )
        )

        # Handle unsuccessful requests
        if not result["success"]:
            return result["message"], status_code

        # Check whether company information exists
        company = result.get("company")

        if company is None:
            return (
                "Please create your company information before adding projects.",
                400
            )

        # Display the Create Project form
        return render_template(
            "createProject.html",
            account_id=account_id,
            username=username,
            company=company
        )

    # Handle Create Project form submission
    def post(self):

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

        # Retrieve submitted project details
        data = request.get_json(silent=True) or {}

        project_name = data.get("project_name", "")
        project_description = data.get("project_description", "")
        progress = data.get("progress", "")
        start_date = data.get("start_date", "")
        end_date = data.get("end_date")

        # Ask the Controller to create the project
        result, status_code = (
            self.create_project_controller.create_project(
                account_id,
                project_name,
                project_description,
                progress,
                start_date,
                end_date
            )
        )

        # Return the Controller's result
        return jsonify(result), status_code
