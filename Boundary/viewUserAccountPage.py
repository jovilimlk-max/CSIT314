
'''
What this code does?
- Retrieve and validate the selected User Account ID.
- Retrieve and prepare the administrator's display name.
- Receive the selected account information from the Controller.
- Display the View User Account HTML page.
- Return an error response if account information cannot be retrieved.
'''

from flask import render_template, jsonify, request


class ViewUserAccountPage:

    # Retrieve and validate the selected Account ID
    def get_account_id(self, account_id):

        # Validate that the Account ID is a positive integer
        if not isinstance(account_id, int) or account_id <= 0:
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
