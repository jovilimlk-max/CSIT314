
'''
What this code does?
- Handle the HTTP GET request for View User Account.
- Retrieve and validate the selected User Account ID.
- Retrieve and prepare the administrator's display name.
- Pass the validated Account ID to the View User Account Controller.
- Receive the selected account information from the Controller.
- Display the View User Account HTML page.
- Return validation and account retrieval errors.
- Does not communicate directly with the Entity.
'''

from flask import render_template, jsonify, request


class ViewUserAccountPage:

    # Store the View User Account Controller
    def __init__(self, view_account_controller):
        self.controller = view_account_controller

    # Handle the View User Account GET request
    def get(self, account_id):

        # Retrieve and validate the selected Account ID
        validated_account_id, error = self.get_account_id(
            account_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass the validated Account ID to the Controller
        result, status_code = self.controller.view_user_account(
            validated_account_id
        )

        # Display the result through the Boundary
        return self.display_account(
            result,
            status_code
        )

    # Retrieve and validate the selected Account ID
    def get_account_id(self, account_id):

        # Validate that the Account ID is a positive integer
        if (
            not isinstance(account_id, int)
            or isinstance(account_id, bool)
            or account_id <= 0
        ):
            return None, {
                "success": False,
                "message": "Invalid user account ID."
            }

        return account_id, None

    # Retrieve and prepare the administrator's display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="User Admin"
        )

        # Strip whitespace and use the default if empty
        username = username.strip()

        if not username:
            username = "User Admin"

        return username

    # Prepare Account ID validation errors for the frontend
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Display the selected User Account
    def display_account(self, result, status_code):

        # Return an error if the account could not be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Retrieve the prepared username
        username = self.get_username()

        # Render the View User Account HTML page
        return render_template(
            "viewUserAccount.html",
            account=result["account"],
            username=username
        ), status_code
