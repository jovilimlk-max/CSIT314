
'''
What this code does?
- Verify that the Interior Designer account exists and is active.
- Retrieve the company associated with the Interior Designer.
- Search projects belonging to that company by project name.
- Support partial and case-insensitive searches.
- Include Ongoing, Completed, Active and Suspended projects.
'''


class SearchProjectController:

    # Store references to the Entity objects
    def __init__(self, project, company_information, user_account):
        self.project = project
        self.company_information = company_information
        self.user_account = user_account

    # Search for projects belonging to the Interior Designer
    def search_projects(self, account_id, search_query=""):

        # Validate account ID
        if not isinstance(account_id, int) or account_id <= 0:
            return {
                "success": False,
                "message": "Invalid account ID."
            }, 400

        # Check whether the user account exists
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Only Interior Designers can search their projects
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can search projects."
            }, 403

        # Suspended accounts cannot manage projects
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Validate the search query
        if not isinstance(search_query, str):
            return {
                "success": False,
                "message": "Invalid search query."
            }, 400

        search_query = search_query.strip()

        if len(search_query) > 255:
            return {
                "success": False,
                "message": "Search query cannot exceed 255 characters."
            }, 400

        # Retrieve all projects belonging to this company
        projects = self.project.get_projects_by_company_id(
            company["company_id"]
        )

        # Search project names without case sensitivity
        if search_query:
            projects = [
                project for project in projects
                if search_query.casefold()
                in project["project_name"].casefold()
            ]

        return {
            "success": True,
            "message": "Projects retrieved successfully.",
            "company": company,
            "projects": projects,
            "search_query": search_query,
            "total_projects": len(projects)
        }, 200
