
'''
What this code does?
- Receive the validated Account ID from the Update User Account Boundary.
- Retrieve existing account details and available profiles from the Entity.
- Receive validated updated account information from the Boundary.
- Pass updated account information to the Entity.
- Return Entity results to the Boundary.
- Support updating account details and assigning or removing profiles.
- Does not handle HTTP requests, validation, HTML,
  password hashing or database operations.
'''


class UpdateUserAccountController:

    # Store the User Account Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Retrieve existing account information for the update form
    def get_account_update_details(self, account_id):

        # Request account information and available profiles from the Entity
        result, status_code = self.user_account.get_account_update_details(
            account_id
        )

        # Return the Entity result to the calling Boundary
        return result, status_code

    # Coordinate updating an existing User Account
    def update_user_account(self, account_id, account_details):

        # Pass validated Account ID and updated details to the Entity
        result = self.user_account.update_account(
            account_id,
            account_details
        )

        # Return the Entity result to the calling Boundary
        return result
