
'''
What this code does?
- Receive a request from the User Accounts Boundary.
- Request all user accounts from the User Account Entity.
- Return the Entity result and status code to the Boundary.
- Support the User Accounts management listing.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class UserAccountsController:

    # Store the User Account Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Coordinate retrieving all user accounts
    def view_all_accounts(self):

        # Request all user accounts from the Entity
        result, status_code = self.user_account.view_all_accounts()

        # Return the result to the calling Boundary
        return result, status_code
