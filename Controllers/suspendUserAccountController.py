
'''
What this code does?
- Receive the validated Account ID and status action from the Suspend User Account Boundary.
- Pass the validated Account ID and action to the User Account Entity.
- Return the Entity result to the Boundary.
- Support suspension and reactivation of User Accounts.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class SuspendUserAccountController:

    # Store the User Account Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Coordinate suspension or reactivation of a User Account
    def change_account_status(self, account_id, action):

        # Pass the validated Account ID and action to the Entity
        result = self.user_account.change_account_status(
            account_id,
            action
        )

        # Return the Entity result to the calling Boundary
        return result
