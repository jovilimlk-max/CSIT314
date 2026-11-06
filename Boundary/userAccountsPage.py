
'''
What this code does?
- Handle the HTTP GET request for the User Accounts page.
- Retrieve and prepare the User Admin's display name.
- Call the User Accounts Controller to retrieve all user accounts.
- Receive user account information returned by the Controller.
- Display the User Accounts management page.
- Pass the accounts and username to the HTML template.
- Return an error if account information cannot be retrieved.
- Does not communicate directly with the Entity.
'''

from flask import render_template, jsonify, request


class UserAccountsPage:

    # Store the User Accounts Controller
    def __init__(self, user_accounts_controller):
        self.controller = user_accounts_controller

    # Handle the User Accounts GET request
    def get(self):

        # Request all user accounts through the Controller
        result, status_code = self.controller.view_all_accounts()

        # Display the result through the Boundary
        return self.display_accounts(
            result,
            status_code
        )

    # Retrieve and prepare the administrator's display name
    def get_username(self):

        # Retrieve the username from the URL
        username = request.args.get(
            "username",
            default="User Admin"
        )

        # Strip whitespace and use the default if empty
        username = username.strip()

        if not username:
            username = "User Admin"

        return username

    # Display the User Accounts management page
    def display_accounts(self, result, status_code):

        # Return an error if account information cannot be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Retrieve the administrator's display name
        username = self.get_username()

        # Render the User Accounts management page
        return render_template(
            "userAccounts.html",
            accounts=result["accounts"],
            username=username
        ), status_code
