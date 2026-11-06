
'''
What this code does?
- Coordinate communication between the Suspend Project Boundary and Entity.
- Handle POST requests to suspend or reactivate projects.
- Retrieve validated Account ID, Project ID and status from the Boundary.
- Pass validated information to the Project Entity.
- Return the Entity result to the Boundary as JSON.
- Support both Current IDP and Past IDP projects.
- Does not perform account checks, validation or database operations.
'''

from flask.views import MethodView


class SuspendProjectController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, suspend_project_boundary, project):
        self.boundary = suspend_project_boundary
        self.project = project

    # Coordinate suspending or reactivating a project
    def post(self, project_id):

        # Retrieve and validate submitted information through the Boundary
        status_details, error = self.boundary.get_status_details(
            project_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(
                error
            )

        # Update the project status through the Entity
        result, status_code = self.project.change_project_status(
            status_details
        )

        # Return the Entity result through the Boundary
        return self.boundary.display_status_result(
            result,
            status_code
        )
