
'''
What this code does?
- Retrieve the username from the URL.
- Strip and prepare the username for display.
- Receive dashboard statistics from the Controller.
- Display the dashboard with the username and statistics.
- Return an error response if statistics cannot be retrieved.
'''

from flask import render_template, jsonify, request


class UserAdminDashboardPage:

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
