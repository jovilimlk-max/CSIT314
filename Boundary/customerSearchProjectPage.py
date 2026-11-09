
'''
What this code does?
- Handle the Customer IDPs page.
- Retrieve and validate the Customer Account ID from the URL.
- Retrieve the Customer's username for display.
- Request all active IDPs and available categories through the Controller.
- Pass the retrieved information to customerSearchProject.html.
- Leave searching, filtering, sorting and pagination to JavaScript.
'''

from flask import request, render_template


class CustomerSearchProjectPage:

    def __init__(self, customer_search_project_controller):

        self.controller = customer_search_project_controller

    # Handle the Customer IDPs page
    def get(self):

        account_id, error = self.get_account_id()

        if error:
            return self.display_validation_error(error)

        # Retrieve all active IDPs without applying UI filters
        search_details = {
            "search_query": "",
            "project_type": "all",
            "category_id": "all",
            "sort_by": "newest"
        }

        result, status_code = self.controller.search_customer_projects(
            search_details
        )

        return self.display_search_results(
            result,
            status_code,
            account_id
        )

    # Retrieve and validate the Customer Account ID
    def get_account_id(self):

        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        if not account_id:
            return None, {
                "success": False,
                "message": "Customer Account ID is required."
            }

        try:
            account_id = int(account_id)

        except ValueError:
            return None, {
                "success": False,
                "message": "Invalid Customer Account ID."
            }

        if account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid Customer Account ID."
            }

        return account_id, None

    # Retrieve the Customer's display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="Customer"
        ).strip()

        return username or "Customer"

    # Display validation errors
    def display_validation_error(self, error):

        return error["message"], 400

    # Render the Customer IDPs page
    def display_search_results(
        self,
        result,
        status_code,
        account_id
    ):

        if not result["success"]:
            return result["message"], status_code

        return render_template(
            "customerSearchProject.html",
            account_id=account_id,
            username=self.get_username(),
            projects=result["projects"],
            categories=result["categories"]
        ), status_code
