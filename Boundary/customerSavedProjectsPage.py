
'''
What this code does?
- Handle GET requests for the Customer Saved IDPs page.
- Extract and validate the Customer Account ID.
- Retrieve saved projects through the Controller.
- Display active saved IDPs using the Customer Saved Projects HTML page.
- Show an empty list when the Customer has no available saved IDPs.
'''

from flask import request, render_template


class CustomerSavedProjectsPage:

    def __init__(self, customer_saved_projects_controller):
        self.controller = customer_saved_projects_controller

    # Handle the Customer Saved IDPs page
    def get(self):

        account_id, error = self.get_account_id()

        if error:
            return self.display_error(error, 400)

        # Retrieve saved IDPs through the Controller
        result, status_code = self.controller.get_saved_projects(
            account_id
        )

        if not result["success"]:
            return self.display_error(
                result["message"],
                status_code
            )

        return self.display_saved_projects(
            result["projects"],
            account_id
        )

    # Retrieve and validate the Customer Account ID
    def get_account_id(self):

        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        if not account_id:
            return None, "Customer Account ID is required."

        try:
            account_id = int(account_id)

        except ValueError:
            return None, "Invalid Customer Account ID."

        if account_id <= 0:
            return None, "Invalid Customer Account ID."

        return account_id, None

    # Retrieve the Customer's display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="Customer"
        ).strip()

        return username or "Customer"

    # Display the Customer's saved IDPs
    def display_saved_projects(self, projects, account_id):

        return render_template(
            "customerSavedProjects.html",
            username=self.get_username(),
            account_id=account_id,
            projects=projects
        ), 200

    # Display validation or retrieval errors
    def display_error(self, message, status_code):

        return message, status_code
