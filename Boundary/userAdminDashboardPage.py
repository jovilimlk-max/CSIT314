
'''
What this code does?
- Handle the HTTP GET request for the User Admin Dashboard.
- Retrieve and prepare the username from the URL.
- Call the User Admin Dashboard Controller to retrieve statistics.
- Receive dashboard statistics returned by the Controller.
- Display total accounts, total profiles and suspended accounts.
- Return an error response if statistics cannot be retrieved.
- Does not communicate directly with the Entity.
'''

from flask import render_template, jsonify, request


class UserAdminDashboardPage:

    # Store the User Admin Dashboard Controller
    def __init__(self, dashboard_controller):
        self.controller = dashboard_controller

    # Handle the User Admin Dashboard GET request
    def get(self):

        # Retrieve the username from the Boundary
        username = self.get_dashboard_details()

        # Request dashboard statistics through the Controller
        result, status_code = self.controller.get_dashboard_statistics()

        # Display the result through the Boundary
        return self.display_dashboard(
            username,
            result,
            status_code
        )

    # Retrieve and prepare the username from the URL
    def get_dashboard_details(self):

        username = request.args.get(
            "username",
            default="User Admin"
        )

        # Strip whitespace and use a default username if empty
        username = username.strip()

        if not username:
            username = "User Admin"

        return username

    # Display the dashboard using results provided by the Controller
    def display_dashboard(self, username, result, status_code):

        # Display an error if dashboard statistics could not be retrieved
        if not result["success"]:
            return jsonify(result), status_code

        # Render the User Admin Dashboard
        return render_template(
            "userAdminDashboard.html",
            username=username,
            statistics=result["statistics"]
        ), status_code
