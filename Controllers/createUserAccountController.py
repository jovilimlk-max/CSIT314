
'''
What this code does?
- Receive validated user account details from the Create User Account Boundary.
- Pass the validated account details to the User Account Entity.
- Return the Entity result to the Boundary.
- Does not handle HTTP requests, input validation, HTML,
  password hashing or database operations.
'''


class CreateUserAccountController:

    # Store the User Account Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Coordinate the creation of a new User Account
    def create_user_account(self, account_details):

        # Pass validated account information to the Entity
        result = self.user_account.create_account(
            account_details
        )

        # Return the Entity result to the calling Boundary
        return result
