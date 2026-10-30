
'''
What this code does?
- Check whether the user account exists.
- Verify that the account belongs to an Interior Designer.
- Retrieve the company information associated with the account.
- Return the company information or an appropriate error.
'''


class ViewCompanyInformationController:

    # Store references to the Entity objects
    def __init__(self, company_information, user_account):
        self.company_information = company_information
        self.user_account = user_account

    # Coordinate the retrieval of company information
    def view_company_information(self, account_id):

        # Check whether the account exists
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Only Interior Designer accounts can view this company page
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can access company information."
            }, 403

        # Check whether the account is active
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Retrieve company information from the Entity
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # No company information has been created yet
        if company is None:
            return {
                "success": True,
                "message": "No company information has been created yet.",
                "company": None
            }, 200

        # Return the existing company information
        return {
            "success": True,
            "message": "Company information retrieved successfully.",
            "company": company
        }, 200
