'''
What this code does?
- Display the Create IDP Category form.
- Retrieve category name and description from the form.
- Trim whitespace and validate required fields.
- Pass validated information to the Create IDP Category Controller.
- Display errors if category creation fails.
- Redirect to the IDP Category main page after successful creation.
- Keep HTTP handling and validation in the Boundary.
'''

from flask import request, render_template, redirect, url_for


class CreateIDPCategoryPage:

    # Store the Create IDP Category Controller
    def __init__(self, create_idp_category_controller):
        self.controller = create_idp_category_controller

    # Display the Create IDP Category form
    def get(self):

        account_id = request.args.get(
            "account_id", default=""
        ).strip()

        username = request.args.get(
            "username", default="Platform Manager"
        ).strip()

        return render_template(
            "createIDPCategory.html",
            account_id=account_id,
            username=username,
            error=None,
            form_data={}
        )

    # Handle Create IDP Category form submission
    def post(self):

        account_id = request.args.get(
            "account_id", default=""
        ).strip()

        username = request.args.get(
            "username", default="Platform Manager"
        ).strip()

        # Retrieve and trim form inputs
        category_name = request.form.get(
            "category_name", ""
        ).strip()

        category_description = request.form.get(
            "category_description", ""
        ).strip()

        form_data = {
            "category_name": category_name,
            "category_description": category_description
        }

        # Validate required fields
        if not category_name:
            return self.display_error(
                "Category name is required.",
                account_id,
                username,
                form_data
            )

        if not category_description:
            return self.display_error(
                "Category description is required.",
                account_id,
                username,
                form_data
            )

        # Pass validated inputs to Controller
        result, status_code = self.controller.create_category(
            form_data
        )

        # Display errors returned from Entity through Controller
        if not result["success"]:
            return self.display_error(
                result["message"],
                account_id,
                username,
                form_data,
                status_code
            )

        # Return to main IDP Category page after success
        return redirect(
            url_for(
                "platform_manager_categories",
                account_id=account_id,
                username=username
            )
        )

    # Display errors on the Create form
    def display_error(
        self,
        message,
        account_id,
        username,
        form_data,
        status_code=400
    ):

        return render_template(
            "createIDPCategory.html",
            account_id=account_id,
            username=username,
            error=message,
            form_data=form_data
        ), status_code