
'''
What this code does?
- Coordinate communication between the User Accounts Boundary and Entity.
- Request all User Accounts from the Entity.
- Pass the Entity result to the Boundary for display.
- Does not perform database operations, validation or business logic.
'''

from flask.views import MethodView


class UserAccountsController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, accounts_boundary, user_account):
        self.boundary = accounts_boundary
        self.user_account = user_account

    # Coordinate displaying the User Accounts management page
    def get(self):

        # Request all User Accounts from the Entity
        result, status_code = self.user_account.view_all_accounts()

        # Pass the result to the Boundary for display
        return self.boundary.display_accounts(
            result,
            status_code
        )
