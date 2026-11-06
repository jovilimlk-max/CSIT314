
'''
What this code does?
- Coordinate communication between the Create Company Information Boundary and Entity.
- Retrieve validated company information from the Boundary.
- Pass the validated information to the CompanyInformation Entity.
- Pass the Entity result back to the Boundary.
- Does not perform business checks, account validation or database operations.
'''

from flask.views import MethodView


class CreateCompanyInformationController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, create_company_boundary, company_information):
        self.boundary = create_company_boundary
        self.company_information = company_information

    # Coordinate the creation of company information
    def post(self):

        # Retrieve validated company information from the Boundary
        company_details, error = self.boundary.get_company_details()

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(error)

        # Pass validated company information to the Entity
        result = self.company_information.create_company(
            company_details
        )

        # Pass the Entity result to the Boundary
        return self.boundary.display_create_company_result(result)
