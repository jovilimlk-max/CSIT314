
'''
What this code does?
- Receive the validated Interior Designer Account ID from the Create Project Boundary.
- Retrieve company information through the Project Entity.
- Return company information to the Boundary for displaying the Create Project page.
- Receive validated project details from the Boundary.
- Pass validated project details to the Project Entity.
- Return project creation results to the Boundary.
- Support both Current IDP and Past IDP projects.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class CreateProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Retrieve company information for the Create Project page
    def get_create_project_company(self, account_id):

        # Pass the validated Account ID to the Project Entity
        result, status_code = self.project.get_create_project_company(
            account_id
        )

        # Return the result to the calling Boundary
        return result, status_code

    # Coordinate creating a new Current IDP or Past IDP
    def create_project(self, project_details):

        # Pass validated project details to the Project Entity
        result = self.project.create_new_project(
            project_details
        )

        # Return the Entity result to the calling Boundary
        return result
