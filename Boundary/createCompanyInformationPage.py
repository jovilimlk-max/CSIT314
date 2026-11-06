
'''
What this code does?
- Retrieve the Interior Designer's username and account ID from the URL.
- Extract and strip submitted company information.
- Validate required fields, email format and established date.
- Pass validated company information to the Controller.
- Display the Create Company Information HTML page.
- Return validation errors and company creation results to the frontend.
'''

import re
from datetime import date

from flask import request, jsonify, render_template


class CreateCompanyInformationPage:

    # Retrieve and prepare the Interior Designer's username
    def get_username(self):

        username = request.args.get(
            "username",
            "Interior Designer"
        ).strip()

        if not username:
            username = "Interior Designer"

        return username

    # Retrieve and validate the Account ID from the URL
    def get_account_id(self):

        account_id = request.args.get(
            "account_id",
            type=int
        )

        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        return account_id, None

    # Retrieve, clean and validate submitted company information
    def get_company_details(self):

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Define the required company information fields
        field_labels = {
            "company_name": "Company name",
            "company_address": "Company address",
            "working_hours": "Working hours",
            "company_email": "Company email",
            "company_phone": "Company phone number",
            "established_date": "Established date",
            "company_description": "What the company does"
        }

        company_details = {}
        errors = {}

        # Retrieve and strip all submitted text fields
        for field, label in field_labels.items():

            value = data.get(field, "")

            company_details[field] = (
                value.strip() if isinstance(value, str) else ""
            )

            # Validate required fields
            if not company_details[field]:
                errors[field] = f"{label} is required."

        # Retrieve and validate the Account ID
        account_id, account_error = self.get_account_id()

        if account_error:
            errors["account_id"] = "Invalid account ID."

        company_details["account_id"] = account_id

        # Validate company email format
        email = company_details["company_email"]

        if email and not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email
        ):
            errors["company_email"] = (
                "Please enter a valid company email address."
            )

        # Validate the established date
        established_date = company_details["established_date"]

        if established_date:
            try:
                selected_date = date.fromisoformat(established_date)

                if selected_date > date.today():
                    errors["established_date"] = (
                        "Established date cannot be in the future."
                    )

            except ValueError:
                errors["established_date"] = (
                    "Please enter a valid established date."
                )

        # Return validation errors to the Controller
        if errors:
            return None, {
                "success": False,
                "message": "Please correct the highlighted fields.",
                "errors": errors
            }

        # Return validated company information
        return company_details, None

    # Display the Create Company Information page
    def display_create_company_page(self):

        # Retrieve the validated Account ID
        account_id, error = self.get_account_id()

        if error:
            return "Invalid account ID.", 400

        # Retrieve the Interior Designer's username
        username = self.get_username()

        # Display the existing HTML template
        return render_template(
            "createCompanyInformation.html",
            username=username,
            account_id=account_id,
            errors={},
            form_data={}
        )

    # Return validation errors to the frontend
    def display_validation_error(self, error):
        return jsonify(error), 400

    # Return the Entity's company creation result
    def display_create_company_result(self, result):
        return jsonify(result["data"]), result["status_code"]
