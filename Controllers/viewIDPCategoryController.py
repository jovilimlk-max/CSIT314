
'''
What this code does?
- Connect the View IDP Category Boundary to the IDPCategory Entity.
- Receive a validated Category ID from the Boundary.
- Retrieve the selected category's information through the Entity.
- Return the category information to the Boundary.
- Keep HTTP handling and validation in the Boundary.
- Keep database operations in the Entity.
'''


class ViewIDPCategoryController:

    # Store the IDPCategory Entity
    def __init__(self, idp_category):
        self.idp_category = idp_category

    # Retrieve the selected IDP category
    def get_category_by_id(self, category_id):

        return self.idp_category.get_category_by_id(
            category_id
        )
