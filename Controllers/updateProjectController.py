
'''
What this code does?
- Check whether the Interior Designer account exists and is active.
- Verify that the project belongs to the Interior Designer's company.
- Validate the updated project details.
- Update the project information through the Project Entity.
- Preserve the project's existing Active/Suspended status.
'''

from datetime import date


class UpdateProjectController:

    # Store references to the Entity objects
    def __init__(self, project, company_information, user_account):
        self.project = project
        self.company_information = company_information
        self.user_account = user_account

    # Update an existing project's information
    def update_project(self, account_id, project_id, project_name,
                       project_description, progress, start_date,
                       end_date=None):

        # Validate the account ID and project ID
        if not isinstance(account_id, int) or account_id <= 0:
            return {
                "success": False,
                "message": "Invalid account ID."
            }, 400

        if not isinstance(project_id, int) or project_id <= 0:
            return {
                "success": False,
                "message": "Invalid project ID."
            }, 400

        # Check whether the user account exists
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Only Interior Designers can update projects
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can update projects."
            }, 403

        # Suspended user accounts cannot update projects
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Retrieve the company associated with the account
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Retrieve the project
        existing_project = self.project.get_project_by_id(project_id)

        if existing_project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        # Ensure the Interior Designer owns this project
        if existing_project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "You do not have permission to update this project."
            }, 403

        # Validate project name and description
        project_name = str(project_name or "").strip()
        project_description = str(project_description or "").strip()
        progress = str(progress or "").strip()

        errors = {}

        if not project_name:
            errors["project_name"] = "Project name is required."
        elif len(project_name) > 255:
            errors["project_name"] = (
                "Project name cannot exceed 255 characters."
            )

        if not project_description:
            errors["project_description"] = (
                "Project description is required."
            )
        elif len(project_description) > 5000:
            errors["project_description"] = (
                "Project description cannot exceed 5000 characters."
            )

        if progress not in ("Ongoing", "Completed"):
            errors["progress"] = (
                "Please select Ongoing or Completed."
            )

        # Validate Start Date
        parsed_start_date = None

        try:
            parsed_start_date = date.fromisoformat(start_date)
        except (TypeError, ValueError):
            errors["start_date"] = (
                "Please enter a valid start date."
            )

        if parsed_start_date is not None:
            if parsed_start_date > date.today():
                errors["start_date"] = (
                    "Start date cannot be in the future."
                )

        # Validate End Date for completed projects
        if progress == "Completed":
            parsed_end_date = None

            try:
                parsed_end_date = date.fromisoformat(end_date)
            except (TypeError, ValueError):
                errors["end_date"] = (
                    "Please enter a valid end date."
                )

            if parsed_end_date is not None:
                if parsed_end_date > date.today():
                    errors["end_date"] = (
                        "End date cannot be in the future."
                    )
                elif (
                    parsed_start_date is not None
                    and parsed_end_date < parsed_start_date
                ):
                    errors["end_date"] = (
                        "End date cannot be earlier than start date."
                    )

        else:
            # Ongoing projects should not have an End Date
            end_date = None

        # Return validation errors
        if errors:
            return {
                "success": False,
                "message": "Please correct the highlighted fields.",
                "errors": errors
            }, 400

        # Update the project through the Entity
        updated = self.project.update_project(
            project_id,
            project_name,
            project_description,
            progress,
            start_date,
            end_date
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update project information."
            }, 500

        return {
            "success": True,
            "message": "Project updated successfully.",
            "project_id": project_id
        }, 200
