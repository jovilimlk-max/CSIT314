
'''
What this code does?
- Coordinate communication between the View Project Boundary and Entity.
- Retrieve the validated Account ID and Project ID from the Boundary.
- Pass the validated IDs to the Project Entity.
- Retrieve the selected Current IDP or Past IDP through the Entity.
- Return the Entity result to the Boundary for display.
- Does not perform account checks, business logic or database operations.
'''

from flask.views import MethodView


class ViewProjectController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, view_project_boundary, project):
        self.boundary = view_project_boundary
        self.project = project

    # Coordinate displaying an individual project
    def get(self, project_id):

        # Retrieve validated Account ID and Project ID
        view_details, error = self.boundary.get_view_details(
            project_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(error)

        # Retrieve the selected project through the Entity
        result, status_code = self.project.view_project(
            view_details
        )

        # Return the Entity result to the Boundary
        return self.boundary.display_project_page(
            result,
            status_code
        )
