
'''
What this code does?
- Handle requests to view the Projects page.
- Retrieve the Interior Designer account ID and username.
- Ask ViewProjectsController to retrieve the company's projects.
- Pass the company and project information to the frontend.
- Display the Projects listing page.
'''

from flask import request, render_template
from flask.views import MethodView


class ViewProjectsPage(MethodView):

    # Store a reference to the Controller
    def __init__(self, view_projects_controller):
        self.view_projects_controller = view_projects_controller

    # Display the Projects page
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

        # Retrieve projects through the Controller
        result, status_code = (
            self.view_projects_controller.get_projects(
                account_id
            )
        )

        # Handle unsuccessful requests
        if not result["success"]:
            return result["message"], status_code

        # Retrieve company information and projects
        company = result.get("company")
        projects = result.get("projects", [])

        # Display the Projects page
        return render_template(
            "viewProjects.html",
            account_id=account_id,
            username=username,
            company=company,
            projects=projects
        )
