
'''
What this code does?
- Coordinate communication between the User Admin Dashboard Boundary and Entity.
- Retrieve the prepared username from the Boundary.
- Request dashboard statistics from the Entity.
- Pass the Entity result to the Boundary for display.
- Does not perform validation or database operations.
'''

from flask.views import MethodView


class UserAdminDashboardController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, dashboard_boundary, user_account):
        self.boundary = dashboard_boundary
        self.user_account = user_account

    # Coordinate retrieval and display of dashboard information
    def get(self):

        # Retrieve the prepared username from the Boundary
        username = self.boundary.get_dashboard_details()

        # Request all dashboard statistics from the Entity
        result, status_code = self.user_account.get_dashboard_statistics()

        # Pass the result to the Boundary for display
        return self.boundary.display_dashboard(
            username,
            result,
            status_code
        )
