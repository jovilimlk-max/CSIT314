
'''
What this code does?
- Connect the Customer Company Information Boundary to the Project Entity.
- Request active company information for the selected IDP.
- Return the Entity's result to the Boundary.
- Keep database operations and domain checks inside the Entity.
'''


class CustomerViewCompanyController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Retrieve active company information for a Customer's selected IDP
    def view_customer_company(self, project_id):

        return self.project.get_customer_project_company_information(
            project_id
        )
