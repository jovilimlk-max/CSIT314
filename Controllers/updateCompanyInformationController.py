
'''
What this code does?
- Receive the validated Interior Designer Account ID from the Update Company Information Boundary.
- Retrieve existing company information through the Entity.
- Receive validated updated company information from the Boundary.
- Pass updated company information to the Entity.
- Return Entity results to the Boundary.
- Does not handle HTTP requests, input validation, HTML or database operations.
'''


class UpdateCompanyInformationController:

    # Store the Company Information Entity
    def __init__(self, company_information):
        self.company_information = company_information

    # Retrieve existing company information for the update page
    def view_company_information(self, account_id):

        # Request existing company information from the Entity
        result, status_code = self.company_information.view_company(
            account_id
        )

        # Return the result to the calling Boundary
        return result, status_code

    # Coordinate updating company information
    def update_company_information(self, company_details):

        # Pass validated updated company information to the Entity
        result = self.company_information.update_company(
            company_details
        )

        # Return the Entity result to the calling Boundary
        return result
