
'''
What this code does?
- Check whether the user account exists.
- Verify that the account belongs to an Interior Designer.
- Check whether the user account is active.
- Check whether company information exists.
- Validate the requested company status.
- Suspend or reactivate company information through the Entity.
- Return the result to the Boundary.
'''


class SuspendCompanyInformationController:

    # Store references to the Entity objects
    def __init__(self, company_information, user_account):
        self.company_information = company_information
        self.user_account = user_account

    # Coordinate suspending or reactivating company information
    def update_company_status(self, account_id, status):

        # Check whether the user account exists
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Only Interior Designers can change company status
        if account["role"] != "designer":
            return {
                "success": False,
                "message": "Only Interior Designers can change company status."
            }, 403

        # Check whether the individual user account is active
        if account["status"] != "active":
            return {
                "success": False,
                "message": "This user account is suspended."
            }, 403

        # Only accept valid company statuses
        if status not in ["active", "suspended"]:
            return {
                "success": False,
                "message": "Invalid company status."
            }, 400

        # Retrieve the existing company information
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Prevent unnecessary status changes
        if company["status"] == status:
            return {
                "success": False,
                "message": (
                    "Company information is already "
                    + status + "."
                )
            }, 409

        # Ask the Entity to change the company status
        updated = self.company_information.update_company_status(
            account_id,
            status
        )

        if not updated:
            return {
                "success": False,
                "message": "Unable to update company status."
            }, 409

        # Return the appropriate success message
        if status == "suspended":
            message = "Company information suspended successfully."
        else:
            message = "Company information reactivated successfully."

        return {
            "success": True,
            "message": message,
            "status": status
        }, 200
