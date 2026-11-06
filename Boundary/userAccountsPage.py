
'''
What this code does?
- Retrieve and prepare the administrator's display name.
- Receive User Account information from the Controller.
- Display the User Accounts management page.
- Pass the accounts and username to the HTML template.
- Return an error if account information cannot be retrieved.
'''

from flask import render_template, jsonify, request


class UserAccountsPage:

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
