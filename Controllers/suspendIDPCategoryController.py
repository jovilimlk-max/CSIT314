
'''
What this code does?
- Connect the Suspend IDP Category Boundary to the IDPCategory Entity.
- Receive a validated Category ID and new status from the Boundary.
- Pass the status change request to the Entity.
- Return the Entity's result to the Boundary.
- Support both suspension and reactivation.
- Keep HTTP handling and input validation in the Boundary.
- Keep database operations and domain checks in the Entity.
'''


class SuspendIDPCategoryController:

    # Store the IDPCategory Entity
    def __init__(self, idp_category):
        self.idp_category = idp_category

    # Pass the validated status change to the Entity
    def change_category_status(self, category_id, new_status):

        return self.idp_category.change_category_status(
            category_id,
            new_status
        )
