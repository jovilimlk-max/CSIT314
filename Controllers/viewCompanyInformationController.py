
'''
What this code does?
- Coordinate communication between the View Company Information Boundary and Entity.
- Retrieve the validated Account ID from the Boundary.
- Request company information from the Entity.
- Return the result through the Boundary.
- Does not perform account checks, business logic or database operations.
'''

from flask.views import MethodView


class ViewCompanyInformationController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, view_company_boundary, company_information):
        self.boundary = view_company_boundary
        self.company_information = company_information

    # Coordinate displaying the View Company Information page
    def get(self):

        # Retrieve the validated Account ID from the Boundary
        account_id, error = self.boundary.get_account_id()

        # Return Boundary validation errors
        if error:
            return self.boundary.display_validation_error(error)

        # Request company information from the Entity
        result, status_code = self.company_information.view_company(
            account_id
        )

        # Pass the result to the Boundary
        return self.boundary.display_company(
            result,
            status_code
        )
