
'''
What this code does?
- Receive a request from the User Admin Dashboard Boundary.
- Request dashboard statistics from the User Account Entity.
- Return the Entity result and status code to the Boundary.
- Support the dashboard statistics for total accounts, total profiles
  and suspended accounts.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class UserAdminDashboardController:

    # Store the User Account Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Coordinate retrieval of dashboard statistics
    def get_dashboard_statistics(self):

        # Request dashboard statistics from the Entity
        result, status_code = self.user_account.get_dashboard_statistics()

        # Return the result to the calling Boundary
        return result, status_code
