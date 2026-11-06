
'''
What this code does?
- Handle GET and POST requests for Update Company Information.
- Retrieve and validate the Interior Designer's Account ID.
- Retrieve and prepare the Interior Designer's username.
- Extract and strip submitted company information.
- Validate required fields, company email format and established date.
- Call the Update Company Information Controller.
- Display the Update Company Information page with existing details.
- Return validation errors and update results to the frontend.
- Does not directly communicate with the Entity.
'''

import re
from datetime import date

from flask import request, jsonify, render_template


class UpdateCompanyInformationPage:

    # Store the Update Company Information Controller
    def __init__(self, update_company_controller):
        self.controller = update_company_controller

    # Handle the GET request to display existing company information
    def get(self):

        # Retrieve and validate the Account ID
        account_id, error = self.get_account_id()

        if error:
            return self.display_validation_error(error)

        # Call the Controller to retrieve existing company information
        result, status_code = self.controller.view_company_information(
            account_id
        )

        # Display the result through the Boundary
        return self.display_update_company_page(
            result,
            status_code
        )

    # Handle the POST request to update company information
    def post(self):

        # Retrieve and validate submitted company information
        company_details, error = self.get_company_details()

        if error:
            return self.display_field_errors(error)

        # Pass validated information to the Controller
        result = self.controller.update_company_information(
            company_details
        )

        # Return the result through the Boundary
        return self.display_update_result(result)

    # Retrieve and validate the Interior Designer's Account ID
    def get_account_id(self):

        # Retrieve Account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Validate the Account ID
        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        return account_id, None

    # Retrieve and prepare the Interior Designer's username
    def get_username(self):

        # Retrieve username from the URL
        username = request.args.get(
            "username",
            "Interior Designer"
        )

        # Remove unnecessary whitespace
        username = username.strip()

        # Use the default username if empty
        if not username:
            username = "Interior Designer"

        return username

    # Retrieve and validate the submitted company information
    def get_company_details(self):

        # Retrieve submitted JSON data
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Define required company information fields
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

        # Extract, strip and validate required fields
        for field, label in field_labels.items():

            value = data.get(field, "")

            company_details[field] = (
                value.strip() if isinstance(value, str) else ""
            )

            # Check whether the field is empty
            if not company_details[field]:
                errors[field] = f"{label} is required."

        # Retrieve and validate Account ID
        account_id, account_error = self.get_account_id()

        if account_error:
            errors["account_id"] = "Invalid account ID."

        company_details["account_id"] = account_id

        # Validate company email format
        company_email = company_details["company_email"]

        if company_email and not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            company_email
        ):
            errors["company_email"] = (
                "Please enter a valid company email address."
            )

        # Validate established date
        established_date = company_details["established_date"]

        if established_date:

            try:
                selected_date = date.fromisoformat(
                    established_date
                )

                # Established date cannot be in the future
                if selected_date > date.today():
                    errors["established_date"] = (
                        "Established date cannot be in the future."
                    )

            except ValueError:
                errors["established_date"] = (
                    "Please enter a valid established date."
                )

        # Return validation errors through the Boundary
        if errors:
            return None, {
                "success": False,
                "message": "Please correct the highlighted fields.",
                "errors": errors
            }

        # Return validated information
        return company_details, None

    # Display Account ID validation errors
    def display_validation_error(self, error):
        return error["message"], 400

    # Display submitted field validation errors
    def display_field_errors(self, error):
        return jsonify(error), 400

    # Display the Update Company Information form
    def display_update_company_page(self, result, status_code):

        # Return the retrieval error if unsuccessful
        if not result["success"]:
            return result["message"], status_code

        # Retrieve existing company information
        company = result["company"]

        # A company record must exist before it can be updated
        if company is None:
            return "Company information not found.", 404

        # Retrieve Account ID and username for the frontend
        account_id, error = self.get_account_id()
        username = self.get_username()

        # Display the form with existing company information
        return render_template(
            "updateCompanyInformation.html",
            account_id=account_id,
            username=username,
            company=company
        ), 200

    # Return the company update result to the frontend
    def display_update_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]
