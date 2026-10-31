
'''
What this code does?
- Display the Create Project page.
- Retrieve the Interior Designer account ID from the URL.
- Receive the project details submitted by the frontend.
- Validate the account ID and submitted JSON.
- Pass the project details to CreateProjectController.
- Return the result to the frontend.
'''

from flask import request, jsonify, render_template
from flask.views import MethodView


class CreateProjectPage(MethodView):

    # Store references to the Controllers
    def __init__(
        self,
        create_project_controller,
        view_company_controller
    ):
        self.create_project_controller = create_project_controller
        self.view_company_controller = view_company_controller

    # Display the Create Project form
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

        # Verify the account and retrieve company information
        result, status_code = (
            self.view_company_controller.get_company_information(
                account_id
            )
        )

        if not result["success"]:
            return result["message"], status_code

        # Company information must exist before creating projects
        company = result.get("company")

        if company is None:
            return (
                "Please create your company information "
                "before creating a project."
            ), 400

        return render_template(
            "createProject.html",
            account_id=account_id,
            username=username,
            company=company
        )

    # Receive and process the Create Project request
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

        # Retrieve the submitted JSON
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "success": False,
                "message": "Invalid project details."
            }), 400

        # Retrieve project details
        project_name = data.get("project_name", "")
        project_description = data.get("project_description", "")
        progress = data.get("progress", "")
        start_date = data.get("start_date", "")
        end_date = data.get("end_date")

        # Pass the information to the Controller
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

        return jsonify(result), status_code
