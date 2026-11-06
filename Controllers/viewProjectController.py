
'''
What this code does?
- Receive the validated Account ID and Project ID from the View Project Boundary.
- Pass the validated IDs to the Project Entity.
- Retrieve the selected Current IDP or Past IDP through the Entity.
- Return the Entity result to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class ViewProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Coordinate retrieving an individual project
    def view_project(self, view_details):

        # Pass the validated Account ID and Project ID to the Entity
        result, status_code = self.project.view_project(
            view_details
        )

        # Return the Entity result to the calling Boundary
        return result, status_code
