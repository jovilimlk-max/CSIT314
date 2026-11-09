
'''
What this code does?
- Display the Edit IDP Category form with existing information.
- Retrieve and validate the Category ID from the URL.
- Extract and trim the updated Category Name and Description.
- Validate required fields before calling the Controller.
- Pass validated information to the Update IDP Category Controller.
- Display validation and duplicate-category errors.
- Preserve entered information when an update fails.
- Redirect to View IDP Category after a successful update.
- Keep HTTP handling and HTML rendering in the Boundary.
'''

from flask import request, render_template, redirect, url_for


class UpdateIDPCategoryPage:

    # Store the Update IDP Category Controller
    def __init__(self, update_idp_category_controller):
        self.controller = update_idp_category_controller

    # Retrieve navigation information from the URL
    def get_navigation_details(self):

        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        username = request.args.get(
            "username",
            default="Platform Manager"
        ).strip()

        return account_id, username

    # Validate the Category ID
    def validate_category_id(self, category_id):

        try:
            category_id = int(category_id)

        except (TypeError, ValueError):
            return None

        if category_id <= 0:
            return None

        return category_id

    # Display the Edit IDP Category form
    def get(self, category_id):

        account_id, username = self.get_navigation_details()

        # Validate the Category ID in Boundary
        category_id = self.validate_category_id(category_id)

        if category_id is None:
            return "Invalid IDP Category ID.", 400

        # Retrieve existing category information through Controller
        category = self.controller.get_category_by_id(
            category_id
        )

        if category is None:
            return "IDP category not found.", 404

        # Render the Edit form with existing values
        return render_template(
            "updateIDPCategory.html",
            account_id=account_id,
            username=username,
            category=category,
            error=None,
            form_data={
                "category_name": category["category_name"],
                "category_description": category["category_description"]
            }
        )

    # Handle the submitted Update IDP Category form
    def post(self, category_id):

        account_id, username = self.get_navigation_details()

        # Validate the Category ID in Boundary
        category_id = self.validate_category_id(category_id)

        if category_id is None:
            return "Invalid IDP Category ID.", 400

        # Retrieve and trim form inputs
        category_name = request.form.get(
            "category_name",
            ""
        ).strip()

        category_description = request.form.get(
            "category_description",
            ""
        ).strip()

        form_data = {
            "category_name": category_name,
            "category_description": category_description
        }

        # Retrieve existing information through Controller
        category = self.controller.get_category_by_id(
            category_id
        )

        if category is None:
            return "IDP category not found.", 404

        # Validate required fields in Boundary
        if not category_name:
            return self.display_error(
                "Category name is required.",
                account_id,
                username,
                category,
                form_data
            )

        if not category_description:
            return self.display_error(
                "Category description is required.",
                account_id,
                username,
                category,
                form_data
            )

        # Pass validated information to Controller
        category_details = {
            "category_id": category_id,
            "category_name": category_name,
            "category_description": category_description
        }

        result, status_code = self.controller.update_category(
            category_details
        )

        # Display errors returned through Controller
        if not result["success"]:
            return self.display_error(
                result["message"],
                account_id,
                username,
                category,
                form_data,
                status_code
            )

        # Return to the read-only category details page
        return redirect(
            url_for(
                "view_idp_category",
                category_id=category_id,
                account_id=account_id,
                username=username
            )
        )

    # Display an error and preserve the entered values
    def display_error(
        self,
        message,
        account_id,
        username,
        category,
        form_data,
        status_code=400
    ):

        return render_template(
            "updateIDPCategory.html",
            account_id=account_id,
            username=username,
            category=category,
            error=message,
            form_data=form_data
        ), status_code
