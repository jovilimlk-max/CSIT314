
'''
What this code does?
- Coordinate communication between the Update User Account Boundary and Entity.
- Retrieve and validate the selected Account ID through the Boundary.
- Request existing account details and available profiles from the Entity.
- Retrieve validated updated account information from the Boundary.
- Pass the updated information to the Entity.
- Return Entity results through the Boundary.
- Does not perform business validation, password hashing or database operations.
'''

from flask.views import MethodView


class UpdateUserAccountController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, update_account_boundary, user_account):
        self.boundary = update_account_boundary
        self.user_account = user_account

    # Coordinate displaying the Update User Account page
    def get(self, account_id):

        # Retrieve the validated Account ID from the Boundary
        validated_id, error = self.boundary.get_account_id(account_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Request existing account details and available profiles
        result, status_code = self.user_account.get_account_update_details(
            validated_id
        )

        # Pass the result to the Boundary for display
        return self.boundary.display_update_account_page(
            result,
            status_code
        )

    # Coordinate updating the selected User Account
    def post(self, account_id):

        # Retrieve the validated Account ID from the Boundary
        validated_id, error = self.boundary.get_account_id(account_id)

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Retrieve validated account information from the Boundary
        account_details, error = self.boundary.get_account_details()

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Pass validated information to the Entity
        result = self.user_account.update_account(
            validated_id,
            account_details
        )

        # Pass the Entity result to the Boundary
        return self.boundary.display_update_account_result(result)
