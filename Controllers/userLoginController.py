
'''
What this code does?
- Receive validated login details from the User Login Boundary.
- Pass the validated login details to the User Account Entity.
- Return the authentication result to the Boundary.
- Support login authentication for all four user roles.
- Does not handle HTTP requests, input validation, HTML or database operations.
'''


class UserLoginController:

    # Store the User Account Entity
    def __init__(self, user_account):
        self.user_account = user_account

    # Coordinate user login authentication
    def authenticate_login(self, login_details):

        # Pass validated login details to the Entity
        result = self.user_account.authenticate_login(
            login_details
        )

        # Return the Entity result to the calling Boundary
        return result
