
'''
What this code does?
- Receive validated information from the Create Project Boundary.
- Retrieve the Interior Designer's company information through the Project Entity.
- Retrieve active IDP categories for the Create Project dropdown.
- Pass validated Current IDP or Past IDP details to the Project Entity.
- Return Entity results to the Boundary.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class CreateProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Retrieve company information for the Create Project page
    def get_create_project_company(self, account_id):

        # Pass the validated Account ID to the Entity
        result, status_code = self.project.get_create_project_company(
            account_id
        )

        # Return the result to the Boundary
        return result, status_code

    # Retrieve active categories for the category dropdown
    def get_active_categories(self):

        # Retrieve categories through the Project Entity's Category Entity
        categories = self.project.idp_category.get_active_categories()

        # Return the available categories to the Boundary
        return categories

    # Create a Current IDP or Past IDP
    def create_new_project(self, project_details):

        # Pass validated project details to the Entity
        result = self.project.create_new_project(
            project_details
        )

        # Return the creation result to the Boundary
        return result
