
'''
What this code does?
- Coordinate communication between the Update Project Boundary and Entity.
- Handle GET requests to display the Update Project form.
- Handle POST requests to update project information.
- Retrieve validated information from the Boundary.
- Pass validated information to the Project Entity.
- Return Entity results to the Boundary.
- Support updating both Current IDP and Past IDP projects.
- Does not perform account checks, validation or database operations.
'''

from flask.views import MethodView


class UpdateProjectController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, update_project_boundary, project):
        self.boundary = update_project_boundary
        self.project = project

    # Coordinate displaying the Update Project form
    def get(self, project_id):

        # Retrieve validated Account ID and Project ID
        view_details, error = self.boundary.get_view_details(
            project_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_page_validation_error(
                error
            )

        # Retrieve the existing project from the Entity
        result, status_code = self.project.view_project(
            view_details
        )

        # Return the project information to the Boundary
        return self.boundary.display_update_project_page(
            result,
            status_code
        )

    # Coordinate updating an existing project
    def post(self, project_id):

        # Retrieve and validate submitted project information
        project_details, error = self.boundary.get_project_details(
            project_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(
                error
            )

        # Update the project through the Entity
        result = self.project.update_project_details(
            project_details
        )

        # Return the update result to the Boundary
        return self.boundary.display_update_result(
            result
        )
