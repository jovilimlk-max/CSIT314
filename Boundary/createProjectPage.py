
'''
What this code does?
- Handle GET and POST requests for Create IDP.
- Retrieve and validate the Interior Designer's Account ID.
- Retrieve the Interior Designer's username.
- Retrieve active categories through the Controller.
- Pass active categories to the Create IDP HTML page.
- Extract and validate submitted project information.
- Allow optional category assignment using a nullable category_id.
- Validate project name, description, type and dates.
- Pass validated project details to the Controller.
- Display the Create IDP page and return creation results.
- Does not communicate directly with the Entities.
'''

from datetime import date

from flask import request, render_template, jsonify


class CreateProjectPage:

    # Store the Create Project Controller
    def __init__(self, create_project_controller):
        self.controller = create_project_controller

    # Handle GET requests for the Create IDP page
    def get(self):

        # Retrieve and validate the Interior Designer's Account ID
        account_id, error = self.get_account_id()

        if error:
            return self.display_page_validation_error(error)

        # Retrieve the Interior Designer's company
        result, status_code = self.controller.get_create_project_company(
            account_id
        )

        # Retrieve active categories through the Controller
        categories = self.controller.get_active_categories()

        # Display the Create IDP form
        return self.display_create_project_page(
            result,
            status_code,
            categories
        )

    # Handle POST requests for creating an IDP
    def post(self):

        # Extract and validate submitted project details
        project_details, error = self.get_project_details()

        if error:
            return self.display_validation_error(error)

        # Pass validated project details to the Controller
        result = self.controller.create_new_project(
            project_details
        )

        # Return the creation result to the frontend
        return self.display_create_project_result(result)

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

    # Retrieve and prepare the Interior Designer's username
    def get_username(self):

        username = request.args.get(
            "username",
            "Interior Designer"
        )

        # Remove unnecessary whitespace
        username = username.strip()

        if not username:
            username = "Interior Designer"

        return username

    # Retrieve and validate submitted project details
    def get_project_details(self):

        # Retrieve submitted JSON data
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            data = {}

        # Retrieve project fields
        project_name = data.get("project_name", "")
        project_description = data.get("project_description", "")
        project_type = data.get("project_type", "")
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")

        # Retrieve the optional category assignment
        category_id = data.get("category_id")

        # Strip unnecessary whitespace from string fields
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

        # Retrieve and validate Account ID
        account_id, account_error = self.get_account_id()

        if account_error:
            return None, account_error

        # Validate project name
        if not project_name:
            return None, {
                "success": False,
                "message": "Project name is required."
            }

        if len(project_name) > 255:
            return None, {
                "success": False,
                "message": "Project name cannot exceed 255 characters."
            }

        # Validate project description
        if not project_description:
            return None, {
                "success": False,
                "message": "Project description is required."
            }

        if len(project_description) > 5000:
            return None, {
                "success": False,
                "message": "Project description cannot exceed 5000 characters."
            }

        # Validate lowercase project type
        if project_type not in ["current", "past"]:
            return None, {
                "success": False,
                "message": "Please select a valid project type."
            }

        # Validate optional Category ID
        # An empty selection is stored as NULL in SQLite
        if category_id is None or category_id == "":
            category_id = None

        elif isinstance(category_id, bool):
            return None, {
                "success": False,
                "message": "The selected category is unavailable."
            }

        elif isinstance(category_id, int):
            if category_id <= 0:
                return None, {
                    "success": False,
                    "message": "The selected category is unavailable."
                }

        elif isinstance(category_id, str):
            category_id = category_id.strip()

            if not category_id:
                category_id = None

            elif category_id.isdecimal() and int(category_id) > 0:
                category_id = int(category_id)

            else:
                return None, {
                    "success": False,
                    "message": "The selected category is unavailable."
                }

        else:
            return None, {
                "success": False,
                "message": "The selected category is unavailable."
            }

        # Validate required start date
        if not start_date:
            return None, {
                "success": False,
                "message": "Start date is required."
            }

        # Validate start date format
        try:
            parsed_start_date = date.fromisoformat(start_date)

            if parsed_start_date.isoformat() != start_date:
                raise ValueError

        except ValueError:
            return None, {
                "success": False,
                "message": "Please enter a valid start date."
            }

        # Start date cannot be in the future
        if parsed_start_date > date.today():
            return None, {
                "success": False,
                "message": "Start date cannot be in the future."
            }

        # Current IDP requires a start date only
        if project_type == "current":

            end_date = None

        # Past IDP requires both start and end dates
        elif project_type == "past":

            if not end_date:
                return None, {
                    "success": False,
                    "message": "End date is required for Past IDP."
                }

            # Validate end date format
            try:
                parsed_end_date = date.fromisoformat(end_date)

                if parsed_end_date.isoformat() != end_date:
                    raise ValueError

            except ValueError:
                return None, {
                    "success": False,
                    "message": "Please enter a valid end date."
                }

            # End date cannot be earlier than start date
            if parsed_end_date < parsed_start_date:
                return None, {
                    "success": False,
                    "message": "End date cannot be earlier than start date."
                }

            # End date cannot be in the future
            if parsed_end_date > date.today():
                return None, {
                    "success": False,
                    "message": "End date cannot be in the future."
                }

        # Return validated project details including category_id
        project_details = {
            "account_id": account_id,
            "project_name": project_name,
            "project_description": project_description,
            "project_type": project_type,
            "start_date": start_date,
            "end_date": end_date,
            "category_id": category_id
        }

        return project_details, None

    # Display the Create IDP page
    def display_create_project_page(
        self,
        result,
        status_code,
        categories
    ):

        # Return errors if the company does not exist
        if not result["success"]:
            return result["message"], status_code

        # Retrieve the Interior Designer's company
        company = result["company"]

        # Render the page with available categories
        return render_template(
            "createProject.html",
            account_id=self.get_account_id()[0],
            username=self.get_username(),
            company=company,
            categories=categories
        ), 200

    # Return Account ID validation errors for GET requests
    def display_page_validation_error(self, error):
        return error["message"], 400

    # Return validation errors for POST requests
    def display_validation_error(self, error):
        return jsonify(error), 400

    # Return the project creation result
    def display_create_project_result(self, result):
        return jsonify(
            result["data"]
        ), result["status_code"]
