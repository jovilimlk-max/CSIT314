
'''
What this code does?
- Connect the Create IDP Category Boundary to the IDPCategory Entity.
- Receive validated category information from the Boundary.
- Pass the information to the Entity for database operations.
- Return the Entity's result to the Boundary.
- Keep validation in Boundary and database operations in Entity.
'''


class CreateIDPCategoryController:

    # Store the IDPCategory Entity
    def __init__(self, idp_category):
        self.idp_category = idp_category

    # Pass validated category details to the Entity
    def create_category(self, category_details):

        return self.idp_category.create_category(
            category_details
        )
