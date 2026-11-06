
'''
What this code does?
- Coordinate communication between the Login Boundary and UserAccount Entity.
- Retrieve validated login details from the Boundary.
- Pass the validated details to the Entity for authentication.
- Pass the Entity result back to the Boundary for display.
'''

from flask.views import MethodView


class UserLoginController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, login_boundary, user_account):
        self.boundary = login_boundary
        self.user_account = user_account

    # Coordinate the login request
    def post(self):

        # Retrieve validated login details from the Boundary
        login_details, error = self.boundary.get_login_details()

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(error)

        # Pass validated login details to the Entity
        result = self.user_account.authenticate_login(login_details)

        # Pass the Entity result back to the Boundary
        return self.boundary.display_login_result(result)
