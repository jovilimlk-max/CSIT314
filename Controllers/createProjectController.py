
'''
What this code does?
- Coordinate communication between the Create Project Boundary and Entity.
- Retrieve the validated Interior Designer Account ID from the Boundary.
- Request company information through the Project Entity.
- Display the Create Project page through the Boundary.
- Retrieve validated project details from the Boundary.
- Pass validated project details to the Project Entity.
- Return project creation results through the Boundary.
- Support both Current IDP and Past IDP projects.
- Does not perform account checks, validation or database operations.
'''

from flask.views import MethodView


class CreateProjectController(MethodView):

    # Store references to the Boundary and Entity
    def __init__(self, create_project_boundary, project):
        self.boundary = create_project_boundary
        self.project = project

    # Coordinate displaying the Create Project page
    def get(self):

        # Retrieve the validated Account ID from the Boundary
        account_id, error = self.boundary.get_account_id()

        # Return Account ID validation errors through the Boundary
        if error:
            return self.boundary.display_page_validation_error(error)

        # Retrieve company information through the Project Entity
        result, status_code = self.project.get_create_project_company(
            account_id
        )

        # Pass the result to the Boundary to display the form
        return self.boundary.display_create_project_page(
            result,
            status_code
        )

    # Coordinate creating a new project
    def post(self):

        # Retrieve validated project details from the Boundary
        project_details, error = self.boundary.get_project_details()

        # Return validation errors through the Boundary
        if error:
            return self.boundary.display_validation_error(error)

        # Pass validated project details to the Project Entity
        result = self.project.create_new_project(
            project_details
        )

        # Return the project creation result through the Boundary
        return self.boundary.display_create_project_result(
            result
        )
