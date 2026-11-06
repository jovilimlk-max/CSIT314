
'''
What this code does?
- Receive the validated Account ID from the View Company Information Boundary.
- Request company information from the Entity.
- Return the Entity result to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''

class ViewCompanyInformationController:

    # Store the Company Information Entity
    def __init__(self, company_information):
        self.company_information = company_information

    # Retrieve company information through the Entity
    def view_company_information(self, account_id):

        # Pass the validated Account ID to the Entity
        result, status_code = self.company_information.view_company(
            account_id
        )

        # Return the result to the calling Boundary
        return result, status_code
