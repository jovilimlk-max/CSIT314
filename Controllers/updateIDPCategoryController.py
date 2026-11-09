
'''
What this code does?
- Connect the Update IDP Category Boundary to the IDPCategory Entity.
- Retrieve the existing category information for the Edit form.
- Receive validated category information from the Boundary.
- Pass updated information to the Entity.
- Return the Entity's results to the Boundary.
- Keep HTTP handling and validation in Boundary.
- Keep database operations and domain checks in Entity.
'''


class UpdateIDPCategoryController:

    # Store the IDPCategory Entity
    def __init__(self, idp_category):
        self.idp_category = idp_category

    # Retrieve existing category information for the Edit form
    def get_category_by_id(self, category_id):

        return self.idp_category.get_category_by_id(
            category_id
        )

    # Update the selected category
    def update_category(self, category_details):

        return self.idp_category.update_category(
            category_details
        )
