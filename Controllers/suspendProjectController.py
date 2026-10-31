
'''
What this code does?
- Check whether the Interior Designer account exists and is active.
- Verify that the selected project belongs to their company.
- Validate the requested project status.
- Suspend or reactivate a project through the Project Entity.
- Preserve the project's other information.
'''


class SuspendProjectController:

    # Store references to the Entity objects
    def __init__(self, project, company_information, user_account):
        self.project = project
        self.company_information = company_information
        self.user_account = user_account

    # Suspend or reactivate an existing project
    def change_project_status(self, account_id, project_id, status):

        # Validate account ID and project ID
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

        # Only Interior Designers can change project status
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can change project status."
            }, 403

        # Suspended user accounts cannot manage projects
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Retrieve company information
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Retrieve the selected project
        existing_project = self.project.get_project_by_id(project_id)

        if existing_project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        # Verify that the project belongs to the Interior Designer
        if existing_project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "You do not have permission to change this project's status."
            }, 403

        # Only active and suspended are valid statuses
        if not isinstance(status, str) or status not in (
            "active",
            "suspended"
        ):
            return {
                "success": False,
                "message": "Invalid project status."
            }, 400

        # Check whether the project already has the requested status
        if existing_project["status"] == status:
            return {
                "success": False,
                "message": "This project is already " + status + "."
            }, 400

        # Update only the project's status
        updated = self.project.update_project_status(
            project_id,
            status
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update project status."
            }, 500

        # Return the successful status change
        if status == "suspended":
            message = "Project suspended successfully."
        else:
            message = "Project reactivated successfully."

        return {
            "success": True,
            "message": message,
            "project_id": project_id,
            "status": status
        }, 200
