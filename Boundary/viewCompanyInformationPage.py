
'''
What this code does?
- Handle the HTTP GET request for View Company Information.
- Retrieve and validate the Interior Designer's Account ID from the URL.
- Retrieve and prepare the Interior Designer's username.
- Call the View Company Information Controller using the validated Account ID.
- Receive company information results returned by the Controller.
- Display existing company information or an empty state.
- Return validation and company retrieval errors.
- Does not directly communicate with the Entity.
'''

from flask import request, render_template


class ViewCompanyInformationPage:

    # Store the View Company Information Controller
    def __init__(self, view_company_controller):
        self.controller = view_company_controller

    # Handle the View Company Information request
    def get(self):

        # Retrieve and validate the Account ID
        account_id, error = self.get_account_id()

        # Return validation errors
        if error:
            return self.display_validation_error(error)

        # Call the Controller using the validated Account ID
        result, status_code = self.controller.view_company_information(
            account_id
        )

        # Return the result through the Boundary
        return self.display_company(
            result,
            status_code
        )

    # Retrieve and validate the Interior Designer's Account ID
    def get_account_id(self):

        # Retrieve the Account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Validate that the Account ID is a positive integer
        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        # Return the validated Account ID
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

        # Use a default username if empty
        if not username:
            username = "Interior Designer"

        return username

    # Display Account ID validation errors
    def display_validation_error(self, error):
        return error["message"], 400

    # Display the View Company Information page
    def display_company(self, result, status_code):

        # Return an error if company information cannot be retrieved
        if not result["success"]:
            return result["message"], status_code

        # Retrieve the Account ID and username for the HTML page
        account_id, error = self.get_account_id()
        username = self.get_username()

        # Display the existing company information or empty state
        return render_template(
            "viewCompanyInformation.html",
            account_id=account_id,
            username=username,
            company=result["company"]
        ), status_code
