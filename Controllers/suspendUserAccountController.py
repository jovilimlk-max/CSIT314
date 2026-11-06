
'''
What this code does?
- Coordinate communication between the Suspend User Account Boundary and Entity.
- Retrieve the validated Account ID from the Boundary.
- Retrieve the validated suspension or reactivation action from the Boundary.
- Pass the validated information to the Entity.
- Return the Entity result through the Boundary.
- Does not perform business validation or database operations.
'''

from flask.views import MethodView


class SuspendUserAccountController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, suspend_account_boundary, user_account):
        self.boundary = suspend_account_boundary
        self.user_account = user_account

    # Coordinate suspension or reactivation of a User Account
    def post(self, account_id):

        # Retrieve the validated Account ID from the Boundary
        validated_id, error = self.boundary.get_account_id(account_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Retrieve the validated action from the Boundary
        action, error = self.boundary.get_status_action()

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Pass the validated ID and action to the Entity
        result = self.user_account.change_account_status(
            validated_id,
            action
        )

        # Pass the Entity result to the Boundary
        return self.boundary.display_status_result(result)
