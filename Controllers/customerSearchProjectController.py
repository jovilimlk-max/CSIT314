
'''
What this code does?
- Receive validated IDP search criteria from the Customer Search Project Boundary.
- Pass the search criteria to the Project Entity.
- Return the Entity result to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class CustomerSearchProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Retrieve matching IDPs for Customer browsing
    def search_customer_projects(self, search_details):

        # Pass validated search criteria to the Entity
        result, status_code = self.project.search_customer_projects(
            search_details
        )

        # Return the result to the Boundary
        return result, status_code
