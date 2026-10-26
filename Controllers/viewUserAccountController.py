
'''
What this code does?
- Retrieve all existing user accounts.
- Retrieve a specific user account using its ID.
- Ask the UserAccount Entity to retrieve account information.
- Ask the UserProfile Entity to retrieve assigned profile information.
- Return the account retrieval results.
'''


class ViewUserAccountController:

    # Store references to the UserAccount and UserProfile Entities
    def __init__(self, user_account, user_profile):
        self.user_account = user_account
        self.user_profile = user_profile

    # Retrieve all user accounts for the management page
    def get_all_accounts(self):
        accounts = self.user_account.get_all_accounts()

        return {
            "success": True,
            "accounts": accounts
        }, 200

    # Retrieve the details of a selected user account
    def get_account_by_id(self, account_id):
        account = self.user_account.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Retrieve the assigned User Profile, if any
        profile_id = account["profile_id"]

        if profile_id is not None:
            profile = self.user_profile.get_profile_by_id(profile_id)

            account["profile_name"] = (
                profile["profile_name"] if profile else None
            )
        else:
            account["profile_name"] = None

        return {
            "success": True,
            "account": account
        }, 200
