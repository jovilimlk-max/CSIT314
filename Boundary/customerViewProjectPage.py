
'''
What this code does?
- Handle Customer requests to view an individual IDP.
- Validate the Customer Account ID and Project ID.
- Identify whether the IDP was opened from IDPs or Saved List.
- Identify returns from Company Information.
- Retrieve active IDP details through the Controller.
- Increase the view count only for normal project openings.
- Preserve Customer information and back navigation.
'''

from flask import request, render_template
from urllib.parse import urlencode


class CustomerViewProjectPage:

    def __init__(self, customer_view_project_controller):
        self.controller = customer_view_project_controller

    # Display an individual Customer IDP
    def get(self, project_id):

        account_id = self.get_account_id()

        if account_id is None:
            return "Invalid or missing Customer Account ID.", 400

        # Validate the Project ID
        if not isinstance(project_id, int) or project_id <= 0:
            return "Invalid Project ID.", 400

        username = self.get_username()
        source = self.get_source()

        # Do not increase the view count when returning from Company Information
        return_from_company = self.get_return_from_company()
        count_view = not return_from_company

        # Retrieve active project details through the Controller
        result, status_code = self.controller.view_customer_project(
            project_id,
            count_view=count_view
        )

        if not result["success"]:
            return result["message"], status_code

        # Preserve Customer details when navigating back
        parameters = urlencode({
            "account_id": account_id,
            "username": username
        })

        if source == "saved":
            back_url = "/customer/saved-projects?" + parameters
            back_label = "Back to Saved List"
        else:
            back_url = "/customer/projects?" + parameters
            back_label = "Back to IDPs"

        # Display the read-only Customer View IDP page
        return render_template(
            "customerViewProject.html",
            project=result["project"],
            account_id=account_id,
            username=username,
            source=source,
            back_url=back_url,
            back_label=back_label
        ), status_code

    # Validate the Customer Account ID
    def get_account_id(self):

        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        try:
            account_id = int(account_id)
            return account_id if account_id > 0 else None

        except ValueError:
            return None

    # Retrieve the Customer's display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="Customer"
        ).strip()

        return username or "Customer"

    # Identify whether the Customer came from IDPs or Saved List
    def get_source(self):

        source = request.args.get(
            "source",
            default="idps"
        ).strip().lower()

        return "saved" if source == "saved" else "idps"

    # Identify navigation back from Company Information
    def get_return_from_company(self):

        return request.args.get(
            "return_from_company",
            default=""
        ).strip() == "1"
