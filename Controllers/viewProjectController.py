
'''
What this code does?
- Check whether the user account exists and is active.
- Verify that the account belongs to an Interior Designer.
- Retrieve the company associated with the account.
- Retrieve the selected project using its Project ID.
- Verify that the project belongs to the Interior Designer's company.
- Return the project details to the Boundary.
'''


class ViewProjectController:

    # Store references to the Entity objects
    def __init__(self, project, company_information, user_account):
        self.project = project
        self.company_information = company_information
        self.user_account = user_account

    # Retrieve the selected project's information
    def view_project(self, account_id, project_id):

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

        # Only Interior Designers can view their projects
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can view project information."
            }, 403

        # Check whether the user account is active
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
        project = self.project.get_project_by_id(project_id)

        if project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        # Check that the project belongs to the Interior Designer's company
        if project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "You do not have permission to view this project."
            }, 403

        # Return the project details
        return {
            "success": True,
            "message": "Project information retrieved successfully.",
            "company": company,
            "project": project
        }, 200
