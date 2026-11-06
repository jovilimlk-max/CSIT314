
'''
What this code does?
- Receive the validated Interior Designer Account ID from the View Projects Boundary.
- Pass the Account ID to the Project Entity.
- Retrieve company information and associated projects through the Entity.
- Return the Entity result to the Boundary.
- Support both Current IDP and Past IDP project listings.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class ViewProjectsController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Coordinate retrieving the Interior Designer's projects
    def view_projects(self, account_id):

        # Pass the validated Account ID to the Project Entity
        result, status_code = self.project.view_projects(
            account_id
        )

        # Return the Entity result to the calling Boundary
        return result, status_code
