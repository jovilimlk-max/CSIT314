
'''
What this code does?
- Receive the validated Account ID from the View User Account Boundary.
- Pass the validated Account ID to the User Account Entity.
- Retrieve the selected user account and its assigned profile information.
- Return the Entity result and status code to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class ViewUserAccountController:

    # Store the User Account Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Coordinate retrieving an individual User Account
    def view_user_account(self, account_id):

        # Pass the validated Account ID to the Entity
        result, status_code = self.user_account.view_account(
            account_id
        )

        # Return the Entity result to the calling Boundary
        return result, status_code
