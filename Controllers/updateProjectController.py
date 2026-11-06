
'''
What this code does?
- Receive validated Account ID and Project ID from the Update Project Boundary.
- Retrieve existing project information through the Project Entity.
- Receive validated updated project information from the Boundary.
- Pass updated project information to the Project Entity.
- Return Entity results to the Boundary.
- Support updating both Current IDP and Past IDP projects.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class UpdateProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Retrieve existing project information for the update form
    def view_project(self, view_details):

        # Pass validated Account ID and Project ID to the Entity
        result, status_code = self.project.view_project(
            view_details
        )

        # Return the Entity result to the calling Boundary
        return result, status_code

    # Coordinate updating an existing project
    def update_project(self, project_details):

        # Pass validated project information to the Entity
        result = self.project.update_project_details(
            project_details
        )

        # Return the Entity result to the calling Boundary
        return result
