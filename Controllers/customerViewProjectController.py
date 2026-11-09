
'''
What this code does?
- Connect the Customer View Project Boundary to the Project Entity.
- Retrieve the details of an active IDP for a Customer.
- Forward whether the project view count should increase.
- Return the Entity's result to the Boundary.
- Keep validation in Boundary and database operations in Entity.
'''


class CustomerViewProjectController:

    # Store the Project Entity
    def __init__(self, project):
        self.project = project

    # Retrieve Customer IDP details
    def view_customer_project(self, project_id, count_view=True):

        return self.project.view_customer_project(
            project_id,
            count_view=count_view
        )
