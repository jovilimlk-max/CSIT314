
'''
What this code does?
- Coordinate communication between the View User Account Boundary and Entity.
- Retrieve the validated Account ID from the Boundary.
- Request account information from the Entity.
- Pass the Entity result to the Boundary for display.
- Does not perform database operations or business logic.
'''

from flask.views import MethodView


class ViewUserAccountController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, view_account_boundary, user_account):
        self.boundary = view_account_boundary
        self.user_account = user_account

    # Coordinate viewing an individual User Account
    def get(self, account_id):

        # Retrieve the validated Account ID from the Boundary
        validated_id, error = self.boundary.get_account_id(account_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Request account information from the Entity
        result, status_code = self.user_account.view_account(
            validated_id
        )

        # Pass the result to the Boundary for display
        return self.boundary.display_account(
            result,
            status_code
        )
