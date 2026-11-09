
'''
What this code does?
- Handle requests to view an individual IDP category.
- Retrieve the Category ID from the URL.
- Validate the Category ID before passing it to the Controller.
- Retrieve category information through the View IDP Category Controller.
- Display the category's name, description and status in read-only form.
- Handle missing or invalid category records.
- Preserve Platform Manager navigation without Flask sessions.
- Keep HTTP handling, validation and HTML rendering in the Boundary.
'''

from flask import request, render_template


class ViewIDPCategoryPage:

    # Store the View IDP Category Controller
    def __init__(self, view_idp_category_controller):
        self.controller = view_idp_category_controller

    # Display the selected IDP category
    def get(self, category_id):

        # Retrieve navigation information from URL parameters
        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        username = request.args.get(
            "username",
            default="Platform Manager"
        ).strip()

        # Validate the Category ID
        try:
            category_id = int(category_id)

        except (TypeError, ValueError):
            return "Invalid IDP Category ID.", 400

        if category_id <= 0:
            return "Invalid IDP Category ID.", 400

        # Retrieve the category through Controller
        category = self.controller.get_category_by_id(
            category_id
        )

        # Handle categories that do not exist
        if category is None:
            return "IDP category not found.", 404

        # Display category information
        return render_template(
            "viewIDPCategory.html",
            account_id=account_id,
            username=username,
            category=category
        )
