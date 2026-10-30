
'''
What this code does?
- Retrieve the User Admin Dashboard statistics.
- Ask the UserAccount Entity for total and suspended account counts.
- Ask the UserProfile Entity for the total profile count.
- Return the statistics to the Dashboard Boundary.
'''


class UserAdminDashboardController:

    def __init__(self, user_account, user_profile):
        self.user_account = user_account
        self.user_profile = user_profile

    # Retrieve the dashboard statistics from both Entities
    def get_dashboard_statistics(self):
        total_accounts = self.user_account.get_total_accounts()
        total_profiles = self.user_profile.get_total_profiles()
        suspended_accounts = self.user_account.get_suspended_accounts()

        return {
            "success": True,
            "statistics": {
                "total_accounts": total_accounts,
                "total_profiles": total_profiles,
                "suspended_accounts": suspended_accounts
            }
        }, 200
