
'''
What this code does?
- Handle GET and POST requests for Update Project.
- Retrieve and validate the Interior Designer's Account ID.
- Retrieve and validate the selected Project ID.
- Retrieve and prepare the Interior Designer's username.
- Extract and strip submitted project information.
- Validate project name, description, type and dates.
- Support updating both Current IDP and Past IDP.
- Use lowercase 'current' and 'past' project type values.
- Call the Update Project Controller to retrieve existing project information.
- Pass validated updated project information to the Controller.
- Display the Update Project form with existing information.
- Return validation errors and update results to the frontend.
- Does not communicate directly with the Entity.
'''

from datetime import date

from flask import request, render_template, jsonify


class UpdateProjectPage:

    # Store the Update Project Controller
    def __init__(self, update_project_controller):
        self.controller = update_project_controller

    # Handle the GET request to display the Update Project form
    def get(self, project_id):

        # Retrieve and validate the Account ID and Project ID
        view_details, error = self.get_view_details(
            project_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.display_page_validation_error(error)

        # Call the Controller to retrieve existing project information
        result, status_code = self.controller.view_project(
            view_details
        )

        # Display the existing project through the Boundary
        return self.display_update_project_page(
            result,
            status_code
        )

    # Handle the POST request to update project information
    def post(self, project_id):

        # Retrieve and validate submitted project information
        project_details, error = self.get_project_details(
            project_id
        )

        # Return validation errors through the Boundary
        if error:
            return self.display_validation_error(error)

        # Pass validated updated project information to the Controller
        result = self.controller.update_project(
            project_details
        )

        # Return the update result through the Boundary
        return self.display_update_result(result)

    # Retrieve and validate the Interior Designer's Account ID
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

    # Retrieve and validate the selected Project ID
    def get_project_id(self, project_id):

        if (
            not isinstance(project_id, int)
            or isinstance(project_id, bool)
            or project_id <= 0
        ):
            return None, {
                "success": False,
                "message": "Invalid project ID."
            }

        return project_id, None

    # Retrieve and prepare the Interior Designer's username
    def get_username(self):

        username = request.args.get(
            "username",
            "Interior Designer"
        )

        username = username.strip()

        if not username:
            username = "Interior Designer"

        return username

    # Retrieve validated IDs for displaying the Update Project page
    def get_view_details(self, project_id):

        # Validate Account ID
        account_id, account_error = self.get_account_id()

        if account_error:
            return None, account_error

        # Validate Project ID
        validated_project_id, project_error = self.get_project_id(
            project_id
        )

        if project_error:
            return None, project_error

        return {
            "account_id": account_id,
            "project_id": validated_project_id
        }, None

    # Retrieve and validate updated project information
    def get_project_details(self, project_id):

        # Validate the Account ID and Project ID
        view_details, error = self.get_view_details(project_id)

        if error:
            return None, error

        # Retrieve submitted JSON data
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Retrieve project information
        project_name = data.get("project_name", "")
        project_description = data.get("project_description", "")
        project_type = data.get("project_type", "")
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")

        # Strip whitespace from all string fields
        project_name = (
            project_name.strip()
            if isinstance(project_name, str)
            else ""
        )

        project_description = (
            project_description.strip()
            if isinstance(project_description, str)
            else ""
        )

        project_type = (
            project_type.strip()
            if isinstance(project_type, str)
            else ""
        )

        start_date = (
            start_date.strip()
            if isinstance(start_date, str)
            else ""
        )

        end_date = (
            end_date.strip()
            if isinstance(end_date, str)
            else ""
        )

        # Store field validation errors
        errors = {}

        # Validate Project Name
        if not project_name:
            errors["project_name"] = "Project name is required."

        elif len(project_name) > 255:
            errors["project_name"] = (
                "Project name cannot exceed 255 characters."
            )

        # Validate Project Description
        if not project_description:
            errors["project_description"] = (
                "Project description is required."
            )

        elif len(project_description) > 5000:
            errors["project_description"] = (
                "Project description cannot exceed 5000 characters."
            )

        # Validate Project Type
        if project_type not in ("current", "past"):
            errors["project_type"] = (
                "Please select a valid project type."
            )

        # Validate Start Date
        parsed_start_date = None

        if not start_date:
            errors["start_date"] = "Start date is required."

        else:
            try:
                parsed_start_date = date.fromisoformat(
                    start_date
                )

                if parsed_start_date.isoformat() != start_date:
                    raise ValueError

            except ValueError:
                errors["start_date"] = (
                    "Please enter a valid start date."
                )

        # Prevent future start dates
        if (
            parsed_start_date is not None
            and parsed_start_date > date.today()
        ):
            errors["start_date"] = (
                "Start date cannot be in the future."
            )

        # Validate End Date for Past IDP
        if project_type == "past":

            parsed_end_date = None

            if not end_date:
                errors["end_date"] = (
                    "End date is required for Past IDP."
                )

            else:
                try:
                    parsed_end_date = date.fromisoformat(
                        end_date
                    )

                    if parsed_end_date.isoformat() != end_date:
                        raise ValueError

                except ValueError:
                    errors["end_date"] = (
                        "Please enter a valid end date."
                    )

            # Prevent future end dates
            if (
                parsed_end_date is not None
                and parsed_end_date > date.today()
            ):
                errors["end_date"] = (
                    "End date cannot be in the future."
                )

            # Ensure the End Date is not earlier than the Start Date
            elif (
                parsed_end_date is not None
                and parsed_start_date is not None
                and parsed_end_date < parsed_start_date
            ):
                errors["end_date"] = (
                    "End date cannot be earlier than start date."
                )

        # Current IDP must not have an End Date
        elif project_type == "current":
            end_date = None

        # Return any field validation errors
        if errors:
            return None, {
                "success": False,
                "message": "Please correct the highlighted fields.",
                "errors": errors
            }

        # Return validated project information
        project_details = {
            "account_id": view_details["account_id"],
            "project_id": view_details["project_id"],
            "project_name": project_name,
            "project_description": project_description,
            "project_type": project_type,
            "start_date": start_date,
            "end_date": end_date
        }

        return project_details, None

    # Display validation errors for GET requests
    def display_page_validation_error(self, error):

        return error["message"], 400

    # Display validation errors for POST requests
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Display the Update Project page with existing information
    def display_update_project_page(self, result, status_code):

        # Return an error if project retrieval was unsuccessful
        if not result["success"]:
            return result["message"], status_code

        # Retrieve the company and existing project information
        company = result["company"]
        project = result["project"]

        # Retrieve Account ID and username for the frontend
        account_id, error = self.get_account_id()
        username = self.get_username()

        # Display the existing Update Project form
        return render_template(
            "updateProject.html",
            account_id=account_id,
            username=username,
            company=company,
            project=project
        ), status_code

    # Return the project update result to the frontend
    def display_update_result(self, result):

        return jsonify(
            result["data"]
        ), result["status_code"]
