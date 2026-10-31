
'''
What this code does?
- Display the Update Company Information HTML page.
- Retrieve the Interior Designer account ID from the URL.
- Ask the Controller to retrieve existing company information.
- Pre-fill the update form with existing company details.
- Receive updated company information as JSON.
- Validate required fields, email format and established date.
- Ask the Controller to update company information.
- Return the result to the frontend.
'''

import re
from datetime import date

from flask import request, jsonify, render_template
from flask.views import MethodView


class UpdateCompanyInformationPage(MethodView):

    # Receive references to the Controllers
    def __init__(
        self,
        update_company_controller,
        view_company_controller
    ):
        self.update_company_controller = update_company_controller
        self.view_company_controller = view_company_controller

    # Retrieve the updated company details from the request
    def get_company_details(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        fields = [
            "company_name",
            "company_address",
            "working_hours",
            "company_email",
            "company_phone",
            "established_date",
            "company_description"
        ]

        company_details = {}

        for field in fields:
            value = data.get(field, "")

            company_details[field] = (
                value.strip() if isinstance(value, str) else ""
            )

        company_details["account_id"] = request.args.get(
            "account_id",
            type=int
        )

        return company_details

    # Validate the updated company information
    def validate_company_details(self, company_details):
        errors = {}

        field_labels = {
            "company_name": "Company name",
            "company_address": "Company address",
            "working_hours": "Working hours",
            "company_email": "Company email",
            "company_phone": "Company phone number",
            "established_date": "Established date",
            "company_description": "What the company does"
        }

        account_id = company_details["account_id"]

        # Check whether the account ID is valid
        if account_id is None or account_id <= 0:
            errors["account_id"] = "Invalid account ID."

        # Check that all required fields have been completed
        for field, label in field_labels.items():
            if not company_details[field]:
                errors[field] = f"{label} is required."

        # Validate the company email address
        company_email = company_details["company_email"]

        if company_email:
            if not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                company_email
            ):
                errors["company_email"] = (
                    "Please enter a valid company email address."
                )

        # Validate the established date
        established_date = company_details["established_date"]

        if established_date:
            try:
                selected_date = date.fromisoformat(
                    established_date
                )

                if selected_date > date.today():
                    errors["established_date"] = (
                        "Established date cannot be in the future."
                    )

            except ValueError:
                errors["established_date"] = (
                    "Please enter a valid established date."
                )

        return errors

    # Display the Update Company Information page
    def get(self):

        # Retrieve the account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        if account_id is None or account_id <= 0:
            return "Invalid account ID.", 400

        # Retrieve the username for display
        username = request.args.get(
            "username",
            "Interior Designer"
        ).strip()

        if not username:
            username = "Interior Designer"

        # Ask the View Controller to retrieve company information
        result, status_code = (
            self.view_company_controller.view_company_information(
                account_id
            )
        )

        # Handle invalid or suspended user accounts
        if not result["success"]:
            return result["message"], status_code

        # Check that company information exists before editing
        company = result["company"]

        if company is None:
            return "Company information not found.", 404

        # Display the edit page with existing company details
        return render_template(
            "updateCompanyInformation.html",
            account_id=account_id,
            username=username,
            company=company
        ), 200

    # Process the submitted company information updates
    def post(self):

        # Retrieve the updated details
        company_details = self.get_company_details()

        # Validate the submitted information
        errors = self.validate_company_details(
            company_details
        )

        if errors:
            return jsonify({
                "success": False,
                "message": "Please correct the highlighted fields.",
                "errors": errors
            }), 400

        # Ask the Update Controller to save the changes
        result, status_code = (
            self.update_company_controller.update_company_information(
                company_details
            )
        )

        return jsonify(result), status_code
