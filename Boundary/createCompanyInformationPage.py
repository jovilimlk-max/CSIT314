
'''
What this code does?
- Display the Create Company Information HTML page.
- Retrieve the username and account ID from the URL.
- Receive new company information.
- Clean the submitted company information.
- Validate required fields, email format and established date.
- Pass valid company information to the Controller.
- Return the company creation result.
'''

import re
from datetime import date

from flask import request, jsonify, render_template
from flask.views import MethodView


class CreateCompanyInformationPage(MethodView):

    # Receives and stores a reference to the Controller object
    def __init__(self, create_company_controller):
        self.create_company_controller = create_company_controller

    # Retrieve and clean the submitted company details
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

        # Account ID comes from the URL, not the form input
        company_details["account_id"] = request.args.get(
            "account_id",
            type=int
        )

        return company_details

    # Validate the submitted company information
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

        # Check the account ID
        account_id = company_details["account_id"]

        if account_id is None or account_id <= 0:
            errors["account_id"] = "Invalid account ID."

        # Check all required fields
        for field, label in field_labels.items():
            if not company_details[field]:
                errors[field] = f"{label} is required."

        # Validate company email
        email = company_details["company_email"]

        if email and not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email
        ):
            errors["company_email"] = (
                "Please enter a valid company email address."
            )

        # Validate established date
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

        return errors

    # Display the Create Company Information HTML page
    def get(self):
        username = request.args.get(
            "username",
            "Interior Designer"
        ).strip()

        if not username:
            username = "Interior Designer"

        account_id = request.args.get("account_id", type=int)

        if account_id is None or account_id <= 0:
            return "Invalid account ID.", 400

        return render_template(
            "createCompanyInformation.html",
            username=username,
            account_id=account_id,
            errors={},
            form_data={}
        )

    # Process the company creation request
    def post(self):
        company_details = self.get_company_details()

        errors = self.validate_company_details(company_details)

        if errors:
            return jsonify({
                "success": False,
                "message": "Please correct the highlighted fields.",
                "errors": errors
            }), 400

        result, status_code = (
            self.create_company_controller.create_company_information(
                company_details
            )
        )

        return jsonify(result), status_code
