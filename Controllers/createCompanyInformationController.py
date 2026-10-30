
'''
What this code does?
- Verify that the account exists and belongs to an Interior Designer.
- Check whether the account already has company information.
- Ask the Entity to create new company information.
- Return the company creation result.
'''


class CreateCompanyInformationController:

    # Store references to the Entity objects
    def __init__(self, company_information, user_account):
        self.company_information = company_information
        self.user_account = user_account

    # Coordinate the creation of company information
    def create_company_information(self, company_details):
        account_id = company_details["account_id"]

        # Check whether the account exists
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Only Interior Designer accounts can create company information
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can create company information."
            }, 403

        # Do not allow suspended accounts to create company information
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Check whether company information already exists
        if self.company_information.company_exists(account_id):
            return {
                "success": False,
                "message": "Company information already exists for this account."
            }, 409

        # Ask the Entity to create company information
        created = self.company_information.create_company_information(
            account_id,
            company_details["company_name"],
            company_details["company_address"],
            company_details["working_hours"],
            company_details["company_email"],
            company_details["company_phone"],
            company_details["established_date"],
            company_details["company_description"]
        )

        if not created:
            return {
                "success": False,
                "message": "Unable to create company information."
            }, 409

        return {
            "success": True,
            "message": "Company information created successfully."
        }, 201
