
'''
What this code does?
- Handle requests to update an existing project.
- Retrieve the account ID, project ID and username.
- Display the Update Project form with existing project details.
- Pass updated project information to UpdateProjectController.
- Return the result of the update request.
'''

from flask import request, render_template, jsonify
from flask.views import MethodView


class UpdateProjectPage(MethodView):

    # Store references to the Controllers
    def __init__(self, update_project_controller, view_project_controller):
        self.update_project_controller = update_project_controller
        self.view_project_controller = view_project_controller

    # Display the Update Project form
    def get(self, project_id):

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

        # Retrieve the existing project through ViewProjectController
        result, status_code = (
            self.view_project_controller.view_project(
                account_id,
                project_id
            )
        )

        # Handle unsuccessful requests
        if not result["success"]:
            return result["message"], status_code

        # Retrieve the company and project details
        company = result["company"]
        project = result["project"]

        # Display the Update Project form
        return render_template(
            "updateProject.html",
            account_id=account_id,
            username=username,
            company=company,
            project=project
        )

    # Handle submission of updated project information
    def post(self, project_id):

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

        # Ask UpdateProjectController to validate and save changes
        result, status_code = (
            self.update_project_controller.update_project(
                account_id,
                project_id,
                project_name,
                project_description,
                progress,
                start_date,
                end_date
            )
        )

        # Return the Controller's result
        return jsonify(result), status_code
