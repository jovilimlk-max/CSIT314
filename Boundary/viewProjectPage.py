
'''
What this code does?
- Handle requests to view an individual project.
- Retrieve the account ID, project ID and username.
- Call ViewProjectController to retrieve the project details.
- Handle invalid accounts or projects.
- Pass the project information to the frontend.
'''

from flask import request, render_template
from flask.views import MethodView


class ViewProjectPage(MethodView):

    # Store a reference to the Controller
    def __init__(self, view_project_controller):
        self.view_project_controller = view_project_controller

    # Display the selected project's information
    def get(self, project_id):

        # Retrieve account information from the URL
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

        # Retrieve the selected project through the Controller
        result, status_code = (
            self.view_project_controller.view_project(
                account_id,
                project_id
            )
        )

        # Handle unsuccessful requests
        if not result["success"]:
            return result["message"], status_code

        # Retrieve the company and project information
        company = result["company"]
        project = result["project"]

        # Display the View Project page
        return render_template(
            "viewProject.html",
            account_id=account_id,
            username=username,
            company=company,
            project=project
        )
