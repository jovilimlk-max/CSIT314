
'''
What this code does?
- Handle requests to display the Platform Manager's IDP Category page.
- Retrieve all IDP categories through the View IDP Categories Controller.
- Pass category information to the HTML template.
- Display an empty state when no categories exist.
- Preserve the Platform Manager's account ID and username for navigation.
- Keep HTTP handling and HTML rendering in the Boundary.
- Keep database operations in the Entity.
'''

from flask import request, render_template


class ViewIDPCategoriesPage:

    # Store the View IDP Categories Controller
    def __init__(self, view_idp_categories_controller):
        self.controller = view_idp_categories_controller

    # Display the Platform Manager's IDP Category landing page
    def get(self):

        # Retrieve account information from URL parameters
        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        username = request.args.get(
            "username",
            default="Platform Manager"
        ).strip()

        # Retrieve all categories through the Controller
        categories = self.controller.get_all_categories()

        # Render the category listing or empty state
        return render_template(
            "viewIDPCategories.html",
            account_id=account_id,
            username=username,
            categories=categories
        )
