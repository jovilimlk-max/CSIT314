
'''
What this code does?
- Check whether the user account exists.
- Verify that the account belongs to an Interior Designer.
- Check whether the user account is active.
- Retrieve the Interior Designer's company information.
- Retrieve all projects belonging to the company.
- Return the projects to the Boundary.
'''

class ViewProjectsController:

    def __init__(self, project, company_information, user_account):
        self.project = project
        self.company_information = company_information
        self.user_account = user_account

    # Retrieve projects belonging to the Interior Designer's company
    def get_projects(self, account_id):

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
                "message": "Only Interior Designers can view projects."
            }, 403

        # Check whether the user account is active
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Retrieve the company associated with the account
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # No company information has been created yet
        if company is None:
            return {
                "success": True,
                "company": None,
                "projects": []
            }, 200

        # Retrieve all projects belonging to the company
        projects = self.project.get_projects_by_company_id(
            company["company_id"]
        )

        return {
            "success": True,
            "company": company,
            "projects": projects
        }, 200
