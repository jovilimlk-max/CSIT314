
'''
What this code does?
- Connect the Customer Save Project Boundary to the SavedProject Entity.
- Handle requests to save an IDP.
- Handle requests to unsave an IDP.
- Check whether a Customer has already saved an IDP.
- Return Entity results to the Boundary.
- Keep validation in Boundary and database operations in Entity.
'''


class CustomerSaveProjectController:

    # Store the SavedProject Entity
    def __init__(self, saved_project):
        self.saved_project = saved_project

    # Save an IDP for the Customer
    def save_project(self, save_details):

        return self.saved_project.save_project(
            save_details
        )

    # Remove an IDP from the Customer's Saved List
    def unsave_project(self, save_details):

        return self.saved_project.unsave_project(
            save_details
        )

    # Check whether the Customer has already saved an IDP
    def is_project_saved(self, account_id, project_id):

        return self.saved_project.is_project_saved(
            account_id,
            project_id
        )
