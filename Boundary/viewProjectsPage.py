
'''
What this code does?
- Retrieve and validate the Interior Designer's Account ID.
- Retrieve and prepare the Interior Designer's username.
- Receive company and project information from the Controller.
- Display Current IDP and Past IDP projects on the Projects page.
- Display an empty state when no projects exist.
- Display a Create Company Information option when no company exists.
- Return validation and retrieval errors.
- Does not directly communicate with Controllers or Entities.
'''

from flask import request, render_template


class ViewProjectsPage:

    # Retrieve and validate the Interior Designer's Account ID
    def get_account_id(self):

        # Retrieve Account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Validate Account ID
        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        return account_id, None

    # Retrieve and prepare the Interior Designer's username
    def get_username(self):

        # Retrieve username from the URL
        username = request.args.get(
            "username",
            "Interior Designer"
        )

        # Strip unnecessary whitespace
        username = username.strip()

        # Use the default username if empty
        if not username:
            username = "Interior Designer"

        return username

    # Display Account ID validation errors
    def display_validation_error(self, error):

        return error["message"], 400

    # Display the Projects listing page
    def display_projects_page(self, result, status_code):

        # Return an error if project retrieval was unsuccessful
        if not result["success"]:
            return result["message"], status_code

        # Retrieve the company and its projects
        company = result.get("company")
        projects = result.get("projects", [])

        # Retrieve Account ID and username for the frontend
        account_id, error = self.get_account_id()
        username = self.get_username()

        # Display Current IDP and Past IDP projects
        return render_template(
            "viewProjects.html",
            account_id=account_id,
            username=username,
            company=company,
            projects=projects
        ), status_code
