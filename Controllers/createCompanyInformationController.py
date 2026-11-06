
'''
What this code does?
- Receive validated company information from the Create Company Information Boundary.
- Pass the validated company information to the Company Information Entity.
- Return the Entity result to the Boundary.
- Does not handle HTTP requests, input validation, HTML or database operations.
'''


class CreateCompanyInformationController:

    # Store the Company Information Entity
    def __init__(self, company_information):
        self.company_information = company_information

    # Coordinate the creation of company information
    def create_company_information(self, company_details):

        # Pass the validated company information to the Entity
        result = self.company_information.create_company(
            company_details
        )

        # Return the Entity result to the calling Boundary
        return result
