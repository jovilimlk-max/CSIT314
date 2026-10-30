
'''
What this code does?
- Display the User Admin Dashboard page.
- Retrieve the username from the URL.
- Request dashboard statistics from the Controller.
- Pass the username and statistics to the HTML page.
- Return an error if the statistics cannot be retrieved.
'''

from flask import render_template, jsonify, request
from flask.views import MethodView


class UserAdminDashboardPage(MethodView):

    def __init__(self, dashboard_controller):
        self.dashboard_controller = dashboard_controller

    # Retrieve the username and dashboard statistics
    def get(self):
        username = request.args.get("username", "User Admin").strip()

        if not username:
            username = "User Admin"

        result, status_code = (
            self.dashboard_controller.get_dashboard_statistics()
        )

        if not result["success"]:
            return jsonify(result), status_code

        return render_template(
            "userAdminDashboard.html",
            username=username,
            statistics=result["statistics"]
        ), status_code
