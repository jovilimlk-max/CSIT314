
'''
What this code does?
- Initialise Flask and the Renovo databases.
- Connect Entity, Controller and Boundary classes.
- Register Flask routes through their respective Boundaries.
- Follow the BCE architecture: Boundary -> Controller -> Entity.
- Return Entity results through Controller -> Boundary.
- Support Login, User Admin, Company Information and Projects.
- Support Current IDP and Past IDP using the project_type field.
- Preserve existing URLs and frontend functionality.
- Avoid Flask sessions and repeated post-login account checks.
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

    # Initialise Flask and connect the BCE layers
    def __init__(self):

        self.app = Flask(
            __name__,
            template_folder="FrontEnd"
        )

        # ==========================================
        # Initialise Entities and databases
        # ==========================================

        self.user_account = UserAccount()
        self.user_account.initialise_database()

        self.user_profile = UserProfile()
        self.user_profile.initialise_database()

        self.company_information = CompanyInformation()
        self.company_information.initialise_database()

        self.project = Project()
        self.project.initialise_database()

        # ==========================================
        # Initialise Controllers
        # Controllers communicate only with Entities
        # ==========================================

        # Login and Dashboard Controllers
        self.login_controller = UserLoginController(
            self.user_account
        )

        self.dashboard_controller = UserAdminDashboardController(
            self.user_account
        )

        # User Account Controllers
        self.accounts_controller = UserAccountsController(
            self.user_account
        )

        self.create_account_controller = CreateUserAccountController(
            self.user_account
        )

        self.view_account_controller = ViewUserAccountController(
            self.user_account
        )

        self.update_account_controller = UpdateUserAccountController(
            self.user_account
        )

        self.suspend_account_controller = SuspendUserAccountController(
            self.user_account
        )

        # User Profile Controllers
        self.profiles_controller = UserProfilesController(
            self.user_profile
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

        # Company Information Controllers
        self.create_company_controller = CreateCompanyInformationController(
            self.company_information
        )

        self.view_company_controller = ViewCompanyInformationController(
            self.company_information
        )

        self.update_company_controller = UpdateCompanyInformationController(
            self.company_information
        )

        self.suspend_company_controller = SuspendCompanyInformationController(
            self.company_information
        )

        # Project Controllers
        self.create_project_controller = CreateProjectController(
            self.project
        )

        self.view_projects_controller = ViewProjectsController(
            self.project
        )

        self.view_project_controller = ViewProjectController(
            self.project
        )

        self.update_project_controller = UpdateProjectController(
            self.project
        )

        self.suspend_project_controller = SuspendProjectController(
            self.project
        )

        self.search_project_controller = SearchProjectController(
            self.project
        )

        # ==========================================
        # Initialise Boundaries
        # Boundaries communicate only with Controllers
        # ==========================================

        # Login and Dashboard Boundaries
        self.login_boundary = UserLoginPage(
            self.login_controller
        )

        self.dashboard_boundary = UserAdminDashboardPage(
            self.dashboard_controller
        )

        # User Account Boundaries
        self.accounts_boundary = UserAccountsPage(
            self.accounts_controller
        )

        self.create_account_boundary = CreateUserAccountPage(
            self.create_account_controller
        )

        self.view_account_boundary = ViewUserAccountPage(
            self.view_account_controller
        )

        self.update_account_boundary = UpdateUserAccountPage(
            self.update_account_controller
        )

        self.suspend_account_boundary = SuspendUserAccountPage(
            self.suspend_account_controller
        )

        # User Profile Boundaries
        self.profiles_boundary = UserProfilesPage(
            self.profiles_controller
        )

        self.create_profile_boundary = CreateUserProfilePage(
            self.create_profile_controller
        )

        self.view_profile_boundary = ViewUserProfilePage(
            self.view_profile_controller
        )

        self.update_profile_boundary = UpdateUserProfilePage(
            self.update_profile_controller
        )

        self.suspend_profile_boundary = SuspendUserProfilePage(
            self.suspend_profile_controller
        )

        # Company Information Boundaries
        self.create_company_boundary = CreateCompanyInformationPage(
            self.create_company_controller
        )

        self.view_company_boundary = ViewCompanyInformationPage(
            self.view_company_controller
        )

        self.update_company_boundary = UpdateCompanyInformationPage(
            self.update_company_controller
        )

        self.suspend_company_boundary = SuspendCompanyInformationPage(
            self.suspend_company_controller
        )

        # Project Boundaries
        self.create_project_boundary = CreateProjectPage(
            self.create_project_controller
        )

        self.view_projects_boundary = ViewProjectsPage(
            self.view_projects_controller
        )

        self.view_project_boundary = ViewProjectPage(
            self.view_project_controller
        )

        self.update_project_boundary = UpdateProjectPage(
            self.update_project_controller
        )

        self.suspend_project_boundary = SuspendProjectPage(
            self.suspend_project_controller
        )

        self.search_project_boundary = SearchProjectPage(
            self.search_project_controller
        )

        # Register all Flask routes
        self.register_routes()

    # ==========================================
    # Register Flask routes through Boundaries
    # ==========================================

    def register_routes(self):

        # ------------------------------------------
        # Login
        # ------------------------------------------

        # Display the Login page
        self.app.add_url_rule(
            "/",
            endpoint="login_page",
            view_func=self.login_boundary.display_login_page,
            methods=["GET"]
        )

        # Process Login
        self.app.add_url_rule(
            "/login",
            endpoint="user_login",
            view_func=self.login_boundary.post,
            methods=["POST"]
        )

        # ------------------------------------------
        # User Admin Dashboard
        # ------------------------------------------

        self.app.add_url_rule(
            "/user-admin/dashboard",
            endpoint="user_admin_dashboard",
            view_func=self.dashboard_boundary.get,
            methods=["GET"]
        )

        # ------------------------------------------
        # User Account Routes
        # ------------------------------------------

        # View all User Accounts
        self.app.add_url_rule(
            "/user-admin/accounts",
            endpoint="user_accounts",
            view_func=self.accounts_boundary.get,
            methods=["GET"]
        )

        # Display Create User Account page
        self.app.add_url_rule(
            "/user-admin/accounts/create",
            endpoint="create_user_account_page",
            view_func=self.create_account_boundary.display_create_account_page,
            methods=["GET"]
        )

        # Create a User Account
        self.app.add_url_rule(
            "/user-admin/accounts",
            endpoint="create_user_account",
            view_func=self.create_account_boundary.post,
            methods=["POST"]
        )

        # View an individual User Account
        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>",
            endpoint="view_user_account",
            view_func=self.view_account_boundary.get,
            methods=["GET"]
        )

        # Display Update User Account page
        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/edit",
            endpoint="update_user_account_page",
            view_func=self.update_account_boundary.get,
            methods=["GET"]
        )

        # Update a User Account
        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/edit",
            endpoint="update_user_account",
            view_func=self.update_account_boundary.post,
            methods=["POST"]
        )

        # Suspend or Reactivate a User Account
        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/status",
            endpoint="suspend_user_account",
            view_func=self.suspend_account_boundary.post,
            methods=["POST"]
        )

        # ------------------------------------------
        # User Profile Routes
        # ------------------------------------------

        # View all User Profiles
        self.app.add_url_rule(
            "/user-admin/profiles",
            endpoint="user_profiles",
            view_func=self.profiles_boundary.get,
            methods=["GET"]
        )

        # Display Create User Profile page
        self.app.add_url_rule(
            "/user-admin/profiles/create",
            endpoint="create_user_profile_page",
            view_func=self.create_profile_boundary.display_create_profile_page,
            methods=["GET"]
        )

        # Create a User Profile
        self.app.add_url_rule(
            "/user-admin/profiles",
            endpoint="create_user_profile",
            view_func=self.create_profile_boundary.post,
            methods=["POST"]
        )

        # View an individual User Profile
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>",
            endpoint="view_user_profile",
            view_func=self.view_profile_boundary.get,
            methods=["GET"]
        )

        # Display Update User Profile page
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            endpoint="update_user_profile_page",
            view_func=self.update_profile_boundary.get,
            methods=["GET"]
        )

        # Update a User Profile
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            endpoint="update_user_profile",
            view_func=self.update_profile_boundary.post,
            methods=["POST"]
        )

        # Suspend or Reactivate a User Profile
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/status",
            endpoint="suspend_user_profile",
            view_func=self.suspend_profile_boundary.post,
            methods=["POST"]
        )

        # ------------------------------------------
        # Company Information Routes
        # ------------------------------------------

        # Display Create Company Information page
        self.app.add_url_rule(
            "/company/create",
            endpoint="create_company_information_page",
            view_func=self.create_company_boundary.display_create_company_page,
            methods=["GET"]
        )

        # Create Company Information
        self.app.add_url_rule(
            "/company/create",
            endpoint="create_company_information",
            view_func=self.create_company_boundary.post,
            methods=["POST"]
        )

        # View Company Information
        self.app.add_url_rule(
            "/interior-designer/company",
            endpoint="view_company_information",
            view_func=self.view_company_boundary.get,
            methods=["GET"]
        )

        # Display Update Company Information page
        self.app.add_url_rule(
            "/interior-designer/company/edit",
            endpoint="update_company_information_page",
            view_func=self.update_company_boundary.get,
            methods=["GET"]
        )

        # Update Company Information
        self.app.add_url_rule(
            "/interior-designer/company/edit",
            endpoint="update_company_information",
            view_func=self.update_company_boundary.post,
            methods=["POST"]
        )

        # Suspend or Reactivate Company Information
        self.app.add_url_rule(
            "/interior-designer/company/status",
            endpoint="suspend_company_information",
            view_func=self.suspend_company_boundary.post,
            methods=["POST"]
        )

        # ------------------------------------------
        # Interior Designer Project Routes
        # ------------------------------------------

        # View all Current IDP and Past IDP projects
        self.app.add_url_rule(
            "/interior-designer/projects",
            endpoint="view_projects",
            view_func=self.view_projects_boundary.get,
            methods=["GET"]
        )

        # Display Create Project page
        self.app.add_url_rule(
            "/interior-designer/projects/create",
            endpoint="create_project_page",
            view_func=self.create_project_boundary.get,
            methods=["GET"]
        )

        # Create a Current IDP or Past IDP
        self.app.add_url_rule(
            "/interior-designer/projects/create",
            endpoint="create_project",
            view_func=self.create_project_boundary.post,
            methods=["POST"]
        )

        # Search Current IDP and Past IDP projects
        self.app.add_url_rule(
            "/interior-designer/projects/search",
            endpoint="search_project",
            view_func=self.search_project_boundary.get,
            methods=["GET"]
        )

        # View an individual Current IDP or Past IDP
        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>",
            endpoint="view_project",
            view_func=self.view_project_boundary.get,
            methods=["GET"]
        )

        # Display Update Project page
        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>/edit",
            endpoint="update_project_page",
            view_func=self.update_project_boundary.get,
            methods=["GET"]
        )

        # Update a Current IDP or Past IDP
        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>/edit",
            endpoint="update_project",
            view_func=self.update_project_boundary.post,
            methods=["POST"]
        )

        # Suspend or Reactivate a Project
        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>/status",
            endpoint="suspend_project",
            view_func=self.suspend_project_boundary.post,
            methods=["POST"]
        )

    # Run the Flask application
    def run(self):

        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
