
'''
What this code does?
- Handle the HTTP GET request for View Project.
- Retrieve and validate the Interior Designer's Account ID.
- Retrieve and validate the selected Project ID.
- Retrieve and prepare the Interior Designer's username.
- Pass validated Account ID and Project ID to the View Project Controller.
- Receive project and company information returned by the Controller.
- Display the selected Current IDP or Past IDP.
- Return validation and project retrieval errors.
- Does not communicate directly with the Entity.
'''

from flask import request, render_template


class ViewProjectPage:

    # Store the View Project Controller
    def __init__(self, view_project_controller):
        self.controller = view_project_controller

    # Handle the View Project GET request
    def get(self, project_id):

        # Retrieve and validate the Account ID and Project ID
        view_details, error = self.get_view_details(
            project_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass validated details to the Controller
        result, status_code = self.controller.view_project(
            view_details
        )

        # Display the result returned by the Controller
        return self.display_project_page(
            result,
            status_code
        )

    # Retrieve and validate the Interior Designer's Account ID
    def get_account_id(self):

        # Retrieve Account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Check that the Account ID is valid
        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        return account_id, None

    # Retrieve and validate the selected Project ID
    def get_project_id(self, project_id):

        # Check that the Project ID is a positive integer
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

    # Retrieve and prepare the Interior Designer's username
    def get_username(self):

        # Retrieve username from the URL
        username = request.args.get(
            "username",
            "Interior Designer"
        )

        # Remove unnecessary whitespace
        username = username.strip()

        # Use the default username if empty
        if not username:
            username = "Interior Designer"

        return username

    # Retrieve the validated IDs for the Controller
    def get_view_details(self, project_id):

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

        # Return validated details
        return {
            "account_id": account_id,
            "project_id": validated_project_id
        }, None

    # Display validation errors
    def display_validation_error(self, error):

        return error["message"], 400

    # Display the selected project's information
    def display_project_page(self, result, status_code):

        # Return an error if project retrieval was unsuccessful
        if not result["success"]:
            return result["message"], status_code

        # Retrieve company and project information
        company = result["company"]
        project = result["project"]

        # Retrieve Account ID and username for the frontend
        account_id, error = self.get_account_id()
        username = self.get_username()

        # Display the existing View Project page
        return render_template(
            "viewProject.html",
            account_id=account_id,
            username=username,
            company=company,
            project=project
        ), status_code
