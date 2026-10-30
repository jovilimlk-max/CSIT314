
'''
What this code does?
- Display the main User Accounts management page.
- Retrieve the username from the URL.
- Request all user accounts from the Controller.
- Pass the username and account information to the HTML page.
'''

from flask import render_template, jsonify, request
from flask.views import MethodView


class UserAccountsPage(MethodView):

    # Receives and stores a reference to the Controller object
    def __init__(self, view_account_controller):
        self.view_account_controller = view_account_controller

    # Retrieve the username and display all user accounts
    def get(self):
        username = request.args.get("username", "User Admin").strip()

        if not username:
            username = "User Admin"

        result, status_code = self.view_account_controller.get_all_accounts()

        # Return an error if the accounts cannot be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Display the User Accounts management page
        return render_template(
            "userAccounts.html",
            accounts=result["accounts"],
            username=username
        ), status_code
