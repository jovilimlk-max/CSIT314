
'''
What this code does?
- Receive a validated Customer Account ID from the Boundary.
- Retrieve the Customer's saved IDPs through the SavedProject Entity.
- Return the Entity result to the Boundary.
- Keep the Controller limited to coordination between Boundary and Entity.
'''


class CustomerSavedProjectsController:

    def __init__(self, saved_project):
        self.saved_project = saved_project

    # Retrieve the Customer's saved IDPs
    def get_saved_projects(self, account_id):

        return self.saved_project.get_saved_projects(account_id)
