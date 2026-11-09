
'''
What this code does?
- Connect the View IDP Categories Boundary to the IDPCategory Entity.
- Retrieve all IDP categories for the Platform Manager's landing page.
- Return the category records to the Boundary.
- Keep input validation and HTML rendering in Boundary.
- Keep database operations in Entity.
'''


class ViewIDPCategoriesController:

    # Store the IDPCategory Entity
    def __init__(self, idp_category):
        self.idp_category = idp_category

    # Retrieve all IDP categories from the Entity
    def get_all_categories(self):

        return self.idp_category.get_all_categories()
