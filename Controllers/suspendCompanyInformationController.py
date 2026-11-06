
'''
What this code does?
- Receive the validated Account ID and requested status from the Boundary.
- Pass the validated details to the Company Information Entity.
- Return the Entity result to the Boundary.
- Support both suspension and reactivation of company information.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class SuspendCompanyInformationController:

    # Store the Company Information Entity
    def __init__(self, company_information):
        self.company_information = company_information

    # Coordinate suspending or reactivating company information
    def change_company_status(self, status_details):

        # Pass the validated Account ID and status to the Entity
        result = self.company_information.change_company_status(
            status_details
        )

        # Return the Entity result to the calling Boundary
        return result
