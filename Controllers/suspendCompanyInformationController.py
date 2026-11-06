
'''
What this code does?
- Coordinate communication between the Suspend Company Information Boundary and Entity.
- Retrieve the validated Account ID and requested status from the Boundary.
- Pass the validated details to the CompanyInformation Entity.
- Return the Entity result through the Boundary.
- Support both suspension and reactivation of company information.
- Does not perform account checks, business logic or database operations.
'''

from flask.views import MethodView


class SuspendCompanyInformationController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, suspend_company_boundary, company_information):
        self.boundary = suspend_company_boundary
        self.company_information = company_information

    # Coordinate suspending or reactivating company information
    def post(self):

        # Retrieve validated Account ID and status from the Boundary
        status_details, error = self.boundary.get_status_details()

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(error)

        # Pass the validated details to the Entity
        result = self.company_information.change_company_status(
            status_details
        )

        # Return the Entity result through the Boundary
        return self.boundary.display_status_result(result)
