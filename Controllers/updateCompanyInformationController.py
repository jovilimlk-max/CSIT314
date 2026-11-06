
'''
What this code does?
- Coordinate communication between the Update Company Information Boundary and Entity.
- Retrieve the validated Interior Designer Account ID from the Boundary.
- Retrieve existing company information through the Entity.
- Pass validated updated company information to the Entity.
- Return retrieval, validation and update results through the Boundary.
- Does not perform account checks, business logic or database operations.
'''

from flask.views import MethodView


class UpdateCompanyInformationController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, update_company_boundary, company_information):
        self.boundary = update_company_boundary
        self.company_information = company_information

    # Coordinate displaying the Update Company Information page
    def get(self):

        # Retrieve the validated Account ID from the Boundary
        account_id, error = self.boundary.get_account_id()

        # Return Account ID validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(error)

        # Retrieve existing company information from the Entity
        result, status_code = self.company_information.view_company(
            account_id
        )

        # Pass the result to the Boundary to display the update form
        return self.boundary.display_update_company_page(
            result,
            status_code
        )

    # Coordinate updating company information
    def post(self):

        # Retrieve validated updated company details from the Boundary
        company_details, error = self.boundary.get_company_details()

        # Return field validation errors through the Boundary
        if error:
            return self.boundary.display_field_errors(error)

        # Pass validated information to the Entity
        result = self.company_information.update_company(
            company_details
        )

        # Return the Entity result through the Boundary
        return self.boundary.display_update_result(result)
