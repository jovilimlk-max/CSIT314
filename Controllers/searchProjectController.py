
'''
What this code does?
- Coordinate communication between the Search Project Boundary and Entity.
- Handle GET requests to search projects.
- Retrieve validated Account ID and search query from the Boundary.
- Pass validated search details to the Project Entity.
- Return matching Current IDP and Past IDP projects through the Boundary.
- Support empty search queries to retrieve all company projects.
- Does not perform account checks, validation or database operations.
'''

from flask.views import MethodView


class SearchProjectController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, search_project_boundary, project):
        self.boundary = search_project_boundary
        self.project = project

    # Coordinate searching for projects
    def get(self):

        # Retrieve validated search information from the Boundary
        search_details, error = self.boundary.get_search_details()

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(
                error
            )

        # Search for matching projects through the Entity
        result, status_code = self.project.search_projects(
            search_details
        )

        # Return the search results through the Boundary
        return self.boundary.display_search_result(
            result,
            status_code
        )
