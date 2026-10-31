
'''
What this code does?
- Entry point for Flask.
- Initialise Flask and the databases.
- Connect the BCE classes and register the HTTP routes.
'''

from flask import Flask

# Boundaries
from Boundary.userLoginPage import UserLoginPage
from Boundary.userAdminDashboardPage import UserAdminDashboardPage
from Boundary.createUserAccountPage import CreateUserAccountPage
from Boundary.createUserProfilePage import CreateUserProfilePage
from Boundary.userAccountsPage import UserAccountsPage
from Boundary.userProfilesPage import UserProfilesPage
from Boundary.viewUserProfilePage import ViewUserProfilePage
from Boundary.updateUserProfilePage import UpdateUserProfilePage
from Boundary.suspendUserProfilePage import SuspendUserProfilePage
from Boundary.viewUserAccountPage import ViewUserAccountPage
from Boundary.updateUserAccountPage import UpdateUserAccountPage
from Boundary.suspendUserAccountPage import SuspendUserAccountPage
from Boundary.createCompanyInformationPage import CreateCompanyInformationPage
from Boundary.viewCompanyInformationPage import ViewCompanyInformationPage
from Boundary.updateCompanyInformationPage import UpdateCompanyInformationPage
from Boundary.suspendCompanyInformationPage import SuspendCompanyInformationPage

# Controllers
from Controllers.userLoginController import UserLoginController
from Controllers.userAdminDashboardController import UserAdminDashboardController
from Controllers.createUserAccountController import CreateUserAccountController
from Controllers.createUserProfileController import CreateUserProfileController
from Controllers.viewUserProfileController import ViewUserProfileController
from Controllers.updateUserProfileController import UpdateUserProfileController
from Controllers.suspendUserProfileController import SuspendUserProfileController
from Controllers.viewUserAccountController import ViewUserAccountController
from Controllers.updateUserAccountController import UpdateUserAccountController
from Controllers.suspendUserAccountController import SuspendUserAccountController
from Controllers.createCompanyInformationController import CreateCompanyInformationController
from Controllers.viewCompanyInformationController import ViewCompanyInformationController
from Controllers.updateCompanyInformationController import UpdateCompanyInformationController
from Controllers.suspendCompanyInformationController import SuspendCompanyInformationController

# Entities
from Entities.userAccount import UserAccount
from Entities.userProfile import UserProfile
from Entities.companyInformation import CompanyInformation


class RenovoApp:

    # Initialise Flask, create BCE objects and register routes
    def __init__(self):
        self.app = Flask(__name__, template_folder="FrontEnd")

        # Initialise Entities
        self.user_account = UserAccount()
        self.user_account.initialise_database()

        self.user_profile = UserProfile()
        self.user_profile.initialise_database()

        self.company_information = CompanyInformation()
        self.company_information.initialise_database()

        # Initialise Controllers
        self.login_controller = UserLoginController(
            self.user_account,
            self.user_profile
        )

        self.dashboard_controller = UserAdminDashboardController(
            self.user_account,
            self.user_profile
        )

        self.create_account_controller = CreateUserAccountController(
            self.user_account
        )

        self.view_account_controller = ViewUserAccountController(
            self.user_account,
            self.user_profile
        )

        self.update_account_controller = UpdateUserAccountController(
            self.user_account,
            self.user_profile
        )

        self.suspend_account_controller = SuspendUserAccountController(
            self.user_account
        )

        self.create_profile_controller = CreateUserProfileController(
            self.user_profile
        )

        self.view_profile_controller = ViewUserProfileController(
            self.user_profile
        )

        self.update_profile_controller = UpdateUserProfileController(
            self.user_profile
        )

        self.suspend_profile_controller = SuspendUserProfileController(
            self.user_profile
        )

        self.create_company_controller = CreateCompanyInformationController(
            self.company_information,
            self.user_account
        )

        self.view_company_controller = ViewCompanyInformationController(
            self.company_information,
            self.user_account
        )

        self.update_company_controller = UpdateCompanyInformationController(
            self.company_information,
            self.user_account
        )

        self.suspend_company_controller = SuspendCompanyInformationController(
            self.company_information,
            self.user_account
        )

        # Register application routes
        self.register_routes()

    # Connect URLs to their respective Boundary classes
    def register_routes(self):

        # Login Boundary
        login_view = UserLoginPage.as_view(
            "user_login",
            self.login_controller
        )

        self.app.add_url_rule(
            "/",
            view_func=login_view,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/login",
            view_func=login_view,
            methods=["POST"]
        )

        # User Admin Dashboard
        dashboard_view = UserAdminDashboardPage.as_view(
            "user_admin_dashboard",
            self.dashboard_controller
        )

        self.app.add_url_rule(
            "/user-admin/dashboard",
            view_func=dashboard_view,
            methods=["GET"]
        )

        # User Accounts management
        accounts_view = UserAccountsPage.as_view(
            "user_accounts",
            self.view_account_controller
        )

        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=accounts_view,
            methods=["GET"]
        )

        # Create User Account
        create_account_view = CreateUserAccountPage.as_view(
            "create_user_account",
            self.create_account_controller
        )

        self.app.add_url_rule(
            "/user-admin/accounts/create",
            view_func=create_account_view,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=create_account_view,
            methods=["POST"]
        )

        # View User Account
        view_account_view = ViewUserAccountPage.as_view(
            "view_user_account",
            self.view_account_controller
        )

        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>",
            view_func=view_account_view,
            methods=["GET"]
        )

        # Update User Account
        update_account_view = UpdateUserAccountPage.as_view(
            "update_user_account",
            self.update_account_controller,
            self.view_account_controller,
            self.view_profile_controller
        )

        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/edit",
            view_func=update_account_view,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/edit",
            view_func=update_account_view,
            methods=["POST"]
        )

        # Suspend / Reactivate User Account
        suspend_account_view = SuspendUserAccountPage.as_view(
            "suspend_user_account",
            self.suspend_account_controller
        )

        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/status",
            view_func=suspend_account_view,
            methods=["POST"]
        )

        # User Profiles management
        profiles_view = UserProfilesPage.as_view(
            "user_profiles",
            self.view_profile_controller
        )

        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=profiles_view,
            methods=["GET"]
        )

        # Create User Profile
        create_profile_view = CreateUserProfilePage.as_view(
            "create_user_profile",
            self.create_profile_controller
        )

        self.app.add_url_rule(
            "/user-admin/profiles/create",
            view_func=create_profile_view,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=create_profile_view,
            methods=["POST"]
        )

        # View User Profile
        view_profile_view = ViewUserProfilePage.as_view(
            "view_user_profile",
            self.view_profile_controller
        )

        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>",
            view_func=view_profile_view,
            methods=["GET"]
        )

        # Update User Profile
        update_profile_view = UpdateUserProfilePage.as_view(
            "update_user_profile",
            self.update_profile_controller,
            self.view_profile_controller
        )

        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            view_func=update_profile_view,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            view_func=update_profile_view,
            methods=["POST"]
        )

        # Suspend / Reactivate User Profile
        suspend_profile_view = SuspendUserProfilePage.as_view(
            "suspend_user_profile",
            self.suspend_profile_controller
        )

        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/status",
            view_func=suspend_profile_view,
            methods=["POST"]
        )

        # Create Company Information
        create_company_view = CreateCompanyInformationPage.as_view(
            "create_company_information",
            self.create_company_controller
        )

        self.app.add_url_rule(
            "/company/create",
            view_func=create_company_view,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/company/create",
            view_func=create_company_view,
            methods=["POST"]
        )

        # View Company Information
        view_company_view = ViewCompanyInformationPage.as_view(
            "view_company_information",
            self.view_company_controller
        )

        self.app.add_url_rule(
            "/interior-designer/company",
            view_func=view_company_view,
            methods=["GET"]
        )

        # Update Company Information
        update_company_view = UpdateCompanyInformationPage.as_view(
            "update_company_information",
            self.update_company_controller,
            self.view_company_controller
        )

        self.app.add_url_rule(
            "/interior-designer/company/edit",
            view_func=update_company_view,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/interior-designer/company/edit",
            view_func=update_company_view,
            methods=["POST"]
        )

        # Suspend / Reactivate Company Information
        suspend_company_view = SuspendCompanyInformationPage.as_view(
            "suspend_company_information",
            self.suspend_company_controller
        )

        self.app.add_url_rule(
            "/interior-designer/company/status",
            view_func=suspend_company_view,
            methods=["POST"]
        )

    # Start Flask
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
