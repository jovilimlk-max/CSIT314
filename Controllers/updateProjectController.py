
'''
What this code does?
- Receive validated information from the Update Project Boundary.
- Retrieve existing project information through the Project Entity.
- Retrieve active IDP categories for the Edit Project dropdown.
- Pass validated project details to the Project Entity for updating.
- Support updating both Current IDP and Past IDP projects.
- Return Entity results to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class UpdateProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Retrieve existing project information for the Edit Project page
    def view_project(self, view_details):

        # Pass validated Account ID and Project ID to the Entity
        result, status_code = self.project.view_project(
            view_details
        )

        # Return the Entity result to the Boundary
        return result, status_code

    # Retrieve active categories for the Edit Project dropdown
    def get_active_categories(self):

        # Retrieve available categories through the Project Entity
        categories = self.project.idp_category.get_active_categories()

        # Return the categories to the Boundary
        return categories

    # Update an existing Current IDP or Past IDP
    def update_project_details(self, project_details):

        # Pass validated project details to the Entity
        result = self.project.update_project_details(
            project_details
        )

        # Return the Entity result to the Boundary
        return result
