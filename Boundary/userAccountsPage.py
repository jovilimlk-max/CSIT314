
'''
What this code does?
- Display the main User Accounts management page.
- Request all user accounts from the Controller.
- Pass the account information to the HTML page.
'''

from flask import render_template, jsonify
from flask.views import MethodView


class UserAccountsPage(MethodView):

    # Receives and stores a reference to the Controller object
    def __init__(self, view_account_controller):
        self.view_account_controller = view_account_controller

    # Retrieve and display all user accounts
    def get(self):
        result, status_code = self.view_account_controller.get_all_accounts()

        # Return an error if the accounts cannot be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Display the User Accounts management page
        return render_template(
            "userAccounts.html",
            accounts=result["accounts"]
        ), status_code
