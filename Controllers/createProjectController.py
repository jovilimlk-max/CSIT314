
'''
What this code does?
- Check whether the user account exists.
- Verify that the account belongs to an Interior Designer.
- Check whether the user account is active.
- Verify that company information exists.
- Validate the project name and description.
- Validate the selected project progress.
- Validate the start and end dates.
- Link the project to the correct company.
- Create the project through the Project Entity.
- Return the result to the Boundary.
'''

from datetime import datetime


class CreateProjectController:

    def __init__(self, project, company_information, user_account):
        self.project = project
        self.company_information = company_information
        self.user_account = user_account

    # Create a new project
    def create_project(
        self,
        account_id,
        project_name,
        project_description,
        progress,
        start_date,
        end_date=None
    ):

        # Check whether the user account exists
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Only Interior Designers can create projects
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can create projects."
            }, 403

        # Check whether the user account is active
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Check whether company information exists
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": (
                    "Please create your company information "
                    "before creating a project."
                )
            }, 400

        # Validate the project name
        if not isinstance(project_name, str) or not project_name.strip():
            return {
                "success": False,
                "message": "Project name is required."
            }, 400

        project_name = project_name.strip()

        if len(project_name) > 255:
            return {
                "success": False,
                "message": "Project name cannot exceed 255 characters."
            }, 400

        # Validate the project description
        if (
            not isinstance(project_description, str)
            or not project_description.strip()
        ):
            return {
                "success": False,
                "message": "Project description is required."
            }, 400

        project_description = project_description.strip()

        if len(project_description) > 5000:
            return {
                "success": False,
                "message": "Project description cannot exceed 5000 characters."
            }, 400

        # Validate project progress
        if progress not in ["Ongoing", "Completed"]:
            return {
                "success": False,
                "message": "Please select a valid project progress."
            }, 400

        # Validate start date
        if not isinstance(start_date, str) or not start_date.strip():
            return {
                "success": False,
                "message": "Start date is required."
            }, 400

        start_date = start_date.strip()

        try:
            parsed_start_date = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

            if parsed_start_date.isoformat() != start_date:
                raise ValueError

        except ValueError:
            return {
                "success": False,
                "message": "Please enter a valid start date."
            }, 400

        # Start date cannot be in the future
        if parsed_start_date > datetime.now().date():
            return {
                "success": False,
                "message": "Start date cannot be in the future."
            }, 400

        # Validate dates based on project progress
        if progress == "Ongoing":

            # Ongoing projects do not require an end date
            end_date = None

        elif progress == "Completed":

            # Completed projects must have an end date
            if not isinstance(end_date, str) or not end_date.strip():
                return {
                    "success": False,
                    "message": "End date is required for completed projects."
                }, 400

            end_date = end_date.strip()

            try:
                parsed_end_date = datetime.strptime(
                    end_date,
                    "%Y-%m-%d"
                ).date()

                if parsed_end_date.isoformat() != end_date:
                    raise ValueError

            except ValueError:
                return {
                    "success": False,
                    "message": "Please enter a valid end date."
                }, 400

            # End date cannot be before start date
            if parsed_end_date < parsed_start_date:
                return {
                    "success": False,
                    "message": "End date cannot be earlier than start date."
                }, 400

            # Completed projects cannot have future end dates
            if parsed_end_date > datetime.now().date():
                return {
                    "success": False,
                    "message": "End date cannot be in the future."
                }, 400

        # Retrieve the company ID
        company_id = company["company_id"]

        # Create the project through the Entity
        project_id = self.project.create_project(
            company_id,
            project_name,
            project_description,
            progress,
            start_date,
            end_date
        )

        if project_id is None:
            return {
                "success": False,
                "message": "Unable to create project."
            }, 409

        return {
            "success": True,
            "message": "Project created successfully.",
            "project_id": project_id,
            "progress": progress
        }, 201
