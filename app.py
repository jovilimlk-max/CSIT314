
'''
What this code does?
- Initialise Flask and the project databases.
- Connect Boundary, Controller and Entity classes.
- Register routes for Login, User Admin, Company Information and Projects.
- Use the revised BCE architecture for User Admin features.
- Remove redundant User Admin Controller initialisations.
- Preserve existing Interior Designer functionality for later refactoring.
'''

from flask import Flask

# Boundaries
from Boundary.userLoginPage import UserLoginPage
from Boundary.userAdminDashboardPage import UserAdminDashboardPage
from Boundary.userAccountsPage import UserAccountsPage
from Boundary.createUserAccountPage import CreateUserAccountPage
from Boundary.viewUserAccountPage import ViewUserAccountPage
from Boundary.updateUserAccountPage import UpdateUserAccountPage
from Boundary.suspendUserAccountPage import SuspendUserAccountPage
from Boundary.userProfilesPage import UserProfilesPage
from Boundary.createUserProfilePage import CreateUserProfilePage
from Boundary.viewUserProfilePage import ViewUserProfilePage
from Boundary.updateUserProfilePage import UpdateUserProfilePage
from Boundary.suspendUserProfilePage import SuspendUserProfilePage
from Boundary.createCompanyInformationPage import CreateCompanyInformationPage
from Boundary.viewCompanyInformationPage import ViewCompanyInformationPage
from Boundary.updateCompanyInformationPage import UpdateCompanyInformationPage
from Boundary.suspendCompanyInformationPage import SuspendCompanyInformationPage
from Boundary.createProjectPage import CreateProjectPage
from Boundary.viewProjectsPage import ViewProjectsPage
from Boundary.viewProjectPage import ViewProjectPage
from Boundary.updateProjectPage import UpdateProjectPage
from Boundary.suspendProjectPage import SuspendProjectPage
from Boundary.searchProjectPage import SearchProjectPage

# Controllers
from Controllers.userLoginController import UserLoginController
from Controllers.userAdminDashboardController import UserAdminDashboardController
from Controllers.userAccountsController import UserAccountsController
from Controllers.createUserAccountController import CreateUserAccountController
from Controllers.viewUserAccountController import ViewUserAccountController
from Controllers.updateUserAccountController import UpdateUserAccountController
from Controllers.suspendUserAccountController import SuspendUserAccountController
from Controllers.userProfilesController import UserProfilesController
from Controllers.createUserProfileController import CreateUserProfileController
from Controllers.viewUserProfileController import ViewUserProfileController
from Controllers.updateUserProfileController import UpdateUserProfileController
from Controllers.suspendUserProfileController import SuspendUserProfileController
from Controllers.createCompanyInformationController import CreateCompanyInformationController
from Controllers.viewCompanyInformationController import ViewCompanyInformationController
from Controllers.updateCompanyInformationController import UpdateCompanyInformationController
from Controllers.suspendCompanyInformationController import SuspendCompanyInformationController
from Controllers.createProjectController import CreateProjectController
from Controllers.viewProjectsController import ViewProjectsController
from Controllers.viewProjectController import ViewProjectController
from Controllers.updateProjectController import UpdateProjectController
from Controllers.suspendProjectController import SuspendProjectController
from Controllers.searchProjectController import SearchProjectController

# Entities
from Entities.userAccount import UserAccount
from Entities.userProfile import UserProfile
from Entities.companyInformation import CompanyInformation
from Entities.project import Project


class RenovoApp:

    # Initialise Flask, Entities and Boundaries
    def __init__(self):
        self.app = Flask(__name__, template_folder="FrontEnd")

        # Initialise Entities and databases
        self.user_account = UserAccount()
        self.user_account.initialise_database()

        self.user_profile = UserProfile()
        self.user_profile.initialise_database()

        self.company_information = CompanyInformation()
        self.company_information.initialise_database()

        self.project = Project()
        self.project.initialise_database()

        # Initialise User Admin Boundaries
        self.login_boundary = UserLoginPage()
        self.dashboard_boundary = UserAdminDashboardPage()

        # User Account Boundaries
        self.accounts_boundary = UserAccountsPage()
        self.create_account_boundary = CreateUserAccountPage()
        self.view_account_boundary = ViewUserAccountPage()
        self.update_account_boundary = UpdateUserAccountPage()
        self.suspend_account_boundary = SuspendUserAccountPage()

        # User Profile Boundaries
        self.profiles_boundary = UserProfilesPage()
        self.create_profile_boundary = CreateUserProfilePage()
        self.view_profile_boundary = ViewUserProfilePage()
        self.update_profile_boundary = UpdateUserProfilePage()
        self.suspend_profile_boundary = SuspendUserProfilePage()

        # Initialise Company Information Controllers
        # Keep existing implementations until ID refactoring
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

        # Initialise Project Controllers
        # Keep existing implementations until ID refactoring
        self.create_project_controller = CreateProjectController(
            self.project,
            self.company_information,
            self.user_account
        )

        self.view_projects_controller = ViewProjectsController(
            self.project,
            self.company_information,
            self.user_account
        )

        self.view_project_controller = ViewProjectController(
            self.project,
            self.company_information,
            self.user_account
        )

        self.update_project_controller = UpdateProjectController(
            self.project,
            self.company_information,
            self.user_account
        )

        self.suspend_project_controller = SuspendProjectController(
            self.project,
            self.company_information,
            self.user_account
        )

        self.search_project_controller = SearchProjectController(
            self.project,
            self.company_information,
            self.user_account
        )

        # Register Flask routes
        self.register_routes()

    # Connect URLs to Boundaries and Controllers
    def register_routes(self):

        # Display Login page through Boundary
        self.app.add_url_rule(
            "/",
            endpoint="login_page",
            view_func=self.login_boundary.display_login_page,
            methods=["GET"]
        )

        # Process Login through Controller
        login_view = UserLoginController.as_view(
            "user_login",
            self.login_boundary,
            self.user_account
        )

        self.app.add_url_rule(
            "/login",
            view_func=login_view,
            methods=["POST"]
        )

        # Display User Admin Dashboard
        dashboard_view = UserAdminDashboardController.as_view(
            "user_admin_dashboard",
            self.dashboard_boundary,
            self.user_account
        )

        self.app.add_url_rule(
            "/user-admin/dashboard",
            view_func=dashboard_view,
            methods=["GET"]
        )

        # Display User Accounts listing
        accounts_view = UserAccountsController.as_view(
            "user_accounts",
            self.accounts_boundary,
            self.user_account
        )

        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=accounts_view,
            methods=["GET"]
        )

        # Display Create User Account page
        self.app.add_url_rule(
            "/user-admin/accounts/create",
            endpoint="create_user_account_page",
            view_func=self.create_account_boundary.display_create_account_page,
            methods=["GET"]
        )

        # Process Create User Account
        create_account_view = CreateUserAccountController.as_view(
            "create_user_account",
            self.create_account_boundary,
            self.user_account
        )

        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=create_account_view,
            methods=["POST"]
        )

        # View individual User Account
        view_account_view = ViewUserAccountController.as_view(
            "view_user_account",
            self.view_account_boundary,
            self.user_account
        )

        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>",
            view_func=view_account_view,
            methods=["GET"]
        )

        # Update User Account
        update_account_view = UpdateUserAccountController.as_view(
            "update_user_account",
            self.update_account_boundary,
            self.user_account
        )

        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/edit",
            view_func=update_account_view,
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate User Account
        suspend_account_view = SuspendUserAccountController.as_view(
            "suspend_user_account",
            self.suspend_account_boundary,
            self.user_account
        )

        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/status",
            view_func=suspend_account_view,
            methods=["POST"]
        )

        # Display User Profiles listing
        profiles_view = UserProfilesController.as_view(
            "user_profiles",
            self.profiles_boundary,
            self.user_profile
        )

        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=profiles_view,
            methods=["GET"]
        )

        # Display Create User Profile page
        self.app.add_url_rule(
            "/user-admin/profiles/create",
            endpoint="create_user_profile_page",
            view_func=self.create_profile_boundary.display_create_profile_page,
            methods=["GET"]
        )

        # Process Create User Profile
        create_profile_view = CreateUserProfileController.as_view(
            "create_user_profile",
            self.create_profile_boundary,
            self.user_profile
        )

        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=create_profile_view,
            methods=["POST"]
        )

        # View individual User Profile
        view_profile_view = ViewUserProfileController.as_view(
            "view_user_profile",
            self.view_profile_boundary,
            self.user_profile
        )

        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>",
            view_func=view_profile_view,
            methods=["GET"]
        )

        # Update User Profile
        update_profile_view = UpdateUserProfileController.as_view(
            "update_user_profile",
            self.update_profile_boundary,
            self.user_profile
        )

        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            view_func=update_profile_view,
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate User Profile
        suspend_profile_view = SuspendUserProfileController.as_view(
            "suspend_user_profile",
            self.suspend_profile_boundary,
            self.user_profile
        )

        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/status",
            view_func=suspend_profile_view,
            methods=["POST"]
        )

        # Create Company Information
        # Existing ID implementation preserved
        create_company_view = CreateCompanyInformationPage.as_view(
            "create_company_information",
            self.create_company_controller
        )

        self.app.add_url_rule(
            "/company/create",
            view_func=create_company_view,
            methods=["GET", "POST"]
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
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate Company Information
        suspend_company_view = SuspendCompanyInformationPage.as_view(
            "suspend_company_information",
            self.suspend_company_controller
        )

        self.app.add_url_rule(
            "/interior-designer/company/status",
            view_func=suspend_company_view,
            methods=["POST"]
        )

        # Display Projects listing
        view_projects_view = ViewProjectsPage.as_view(
            "view_projects",
            self.view_projects_controller
        )

        self.app.add_url_rule(
            "/interior-designer/projects",
            view_func=view_projects_view,
            methods=["GET"]
        )

        # Create Project
        create_project_view = CreateProjectPage.as_view(
            "create_project",
            self.create_project_controller,
            self.view_company_controller
        )

        self.app.add_url_rule(
            "/interior-designer/projects/create",
            view_func=create_project_view,
            methods=["GET", "POST"]
        )

        # Search Projects
        search_project_view = SearchProjectPage.as_view(
            "search_project",
            self.search_project_controller
        )

        self.app.add_url_rule(
            "/interior-designer/projects/search",
            view_func=search_project_view,
            methods=["GET"]
        )

        # View individual Project
        view_project_view = ViewProjectPage.as_view(
            "view_project",
            self.view_project_controller
        )

        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>",
            view_func=view_project_view,
            methods=["GET"]
        )

        # Update Project
        update_project_view = UpdateProjectPage.as_view(
            "update_project",
            self.update_project_controller,
            self.view_project_controller
        )

        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>/edit",
            view_func=update_project_view,
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate Project
        suspend_project_view = SuspendProjectPage.as_view(
            "suspend_project",
            self.suspend_project_controller
        )

        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>/status",
            view_func=suspend_project_view,
            methods=["POST"]
        )

    # Start Flask
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
