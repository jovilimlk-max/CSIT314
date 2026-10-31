
'''
What this code does?
- Check whether the user account exists.
- Verify that the account belongs to an Interior Designer.
- Check whether the user account is active.
- Check whether company information already exists.
- Update the company's details through the CompanyInformation Entity.
- Return the update result to the Boundary.
'''


class UpdateCompanyInformationController:

    # Store references to the Entity objects
    def __init__(self, company_information, user_account):
        self.company_information = company_information
        self.user_account = user_account

    # Coordinate the updating of company information
    def update_company_information(self, company_details):

        account_id = company_details["account_id"]

        # Check whether the account exists
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Only Interior Designers can update company information
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can update company information."
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
                "message": "Company information not found."
            }, 404

        # Ask the Entity to update the company information
        updated = self.company_information.update_company_information(
            account_id,
            company_details["company_name"],
            company_details["company_address"],
            company_details["working_hours"],
            company_details["company_email"],
            company_details["company_phone"],
            company_details["established_date"],
            company_details["company_description"]
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update company information."
            }, 409

        return {
            "success": True,
            "message": "Company information updated successfully."
        }, 200
