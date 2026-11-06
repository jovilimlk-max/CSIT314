
'''
What this code does?
- Receive validated Account ID and search query from the Search Project Boundary.
- Pass validated search details to the Project Entity.
- Return matching Current IDP and Past IDP projects to the Boundary.
- Support empty search queries to retrieve all company projects.
- Does not handle HTTP requests, validation, HTML or database operations.
'''


class SearchProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Coordinate searching for projects
    def search_projects(self, search_details):

        # Pass validated search details to the Project Entity
        result, status_code = self.project.search_projects(
            search_details
        )

        # Return the Entity result to the calling Boundary
        return result, status_code
