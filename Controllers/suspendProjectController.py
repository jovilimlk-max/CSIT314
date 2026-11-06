
'''
What this code does?
- Receive validated Account ID, Project ID and status from the Suspend Project Boundary.
- Pass validated information to the Project Entity.
- Return the Entity result and status code to the Boundary.
- Support suspension and reactivation of Current IDP and Past IDP projects.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class SuspendProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Coordinate suspending or reactivating a project
    def change_project_status(self, status_details):

        # Pass validated details to the Project Entity
        result, status_code = self.project.change_project_status(
            status_details
        )

        # Return the Entity result to the calling Boundary
        return result, status_code
