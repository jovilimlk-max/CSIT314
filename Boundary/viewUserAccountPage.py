
'''
What this code does?
- Receive the selected user account ID from the URL.
- Validate the account ID.
- Retrieve the username from the URL.
- Request the selected user account details from the Controller.
- Pass the username and account details to the HTML page.
- Return an error if the user account cannot be found.
'''

from flask import render_template, jsonify, request
from flask.views import MethodView


class ViewUserAccountPage(MethodView):

    # Receives and stores a reference to the Controller object
    def __init__(self, view_account_controller):
        self.view_account_controller = view_account_controller

    # Retrieve and display the selected user account
    def get(self, account_id):

        # Validate that the account ID is a positive integer
        if account_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid user account ID."
            }), 400

        # Retrieve the username from the URL
        username = request.args.get("username", "User Admin").strip()

        if not username:
            username = "User Admin"

        # Request the account details from the Controller
        result, status_code = self.view_account_controller.get_account_by_id(
            account_id
        )

        # Return an error if the account does not exist
        if not result["success"]:
            return jsonify(result), status_code

        # Display the selected account information
        return render_template(
            "viewUserAccount.html",
            account=result["account"],
            username=username
        ), status_code
