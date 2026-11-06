
'''
What this code does?
- Coordinate communication between the View Projects Boundary and Entity.
- Retrieve the validated Interior Designer Account ID from the Boundary.
- Pass the Account ID to the Project Entity.
- Retrieve company information and associated projects through the Entity.
- Return the results to the Boundary for display.
- Support both Current IDP and Past IDP project listings.
- Does not perform account checks, business logic or database operations.
'''

from flask.views import MethodView


class ViewProjectsController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, view_projects_boundary, project):
        self.boundary = view_projects_boundary
        self.project = project

    # Coordinate displaying the Projects listing page
    def get(self):

        # Retrieve the validated Account ID from the Boundary
        account_id, error = self.boundary.get_account_id()

        # Return Account ID validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(error)

        # Retrieve company information and projects from the Entity
        result, status_code = self.project.view_projects(
            account_id
        )

        # Pass the result to the Boundary for display
        return self.boundary.display_projects_page(
            result,
            status_code
        )
