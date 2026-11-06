
'''
What this code does?
- Coordinate communication between the Create User Account Boundary and Entity.
- Retrieve validated account information from the Boundary.
- Pass account information to the Entity for creation.
- Pass the Entity result back to the Boundary for display.
- Does not perform validation, password hashing or database operations.
'''

from flask.views import MethodView


class CreateUserAccountController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, create_account_boundary, user_account):
        self.boundary = create_account_boundary
        self.user_account = user_account

    # Coordinate the creation of a new User Account
    def post(self):

        # Retrieve validated account details from the Boundary
        account_details, error = self.boundary.get_account_details()

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Pass validated account information to the Entity
        result = self.user_account.create_account(account_details)

        # Pass the Entity result back to the Boundary
        return self.boundary.display_create_account_result(result)
