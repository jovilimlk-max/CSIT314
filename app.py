
'''
What this code does?
- Initialise Flask and the project databases.
- Connect Boundary, Controller and Entity classes.
- Register routes for Login, User Admin, Company Information and Projects.
- Use the revised BCE architecture for Company Information features.
- Use the revised BCE architecture for Create, View, Update, Suspend and Search Project.
- Support Current IDP and Past IDP using the project_type field.
- Preserve existing User Admin and Company Information functionality.
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

    # Initialise Flask, Entities, Boundaries and Controllers
    def __init__(self):

        self.app = Flask(
            __name__,
            template_folder="FrontEnd"
        )

        # Initialise Entities and databases
        self.user_account = UserAccount()
        self.user_account.initialise_database()

        self.user_profile = UserProfile()
        self.user_profile.initialise_database()

        self.company_information = CompanyInformation()
        self.company_information.initialise_database()

        self.project = Project()
        self.project.initialise_database()

        # Login and User Admin Boundaries
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

        # Company Information Boundaries
        self.create_company_boundary = CreateCompanyInformationPage()
        self.view_company_boundary = ViewCompanyInformationPage()
        self.update_company_boundary = UpdateCompanyInformationPage()
        self.suspend_company_boundary = SuspendCompanyInformationPage()

        # Project Boundaries
        self.create_project_boundary = CreateProjectPage()
        self.view_projects_boundary = ViewProjectsPage()
        self.view_project_boundary = ViewProjectPage()
        self.update_project_boundary = UpdateProjectPage()
        self.suspend_project_boundary = SuspendProjectPage()
        self.search_project_boundary = SearchProjectPage()

        # Register Flask routes
        self.register_routes()

    # Connect Flask URLs to Boundaries and Controllers
    def register_routes(self):

        # Display Login page
        self.app.add_url_rule(
            "/",
            endpoint="login_page",
            view_func=self.login_boundary.display_login_page,
            methods=["GET"]
        )

        # Process Login
        self.app.add_url_rule(
            "/login",
            view_func=UserLoginController.as_view(
                "user_login",
                self.login_boundary,
                self.user_account
            ),
            methods=["POST"]
        )

        # User Admin Dashboard
        self.app.add_url_rule(
            "/user-admin/dashboard",
            view_func=UserAdminDashboardController.as_view(
                "user_admin_dashboard",
                self.dashboard_boundary,
                self.user_account
            ),
            methods=["GET"]
        )

        # View User Accounts listing
        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=UserAccountsController.as_view(
                "user_accounts",
                self.accounts_boundary,
                self.user_account
            ),
            methods=["GET"]
        )

        # Display Create User Account page
        self.app.add_url_rule(
            "/user-admin/accounts/create",
            endpoint="create_user_account_page",
            view_func=self.create_account_boundary.display_create_account_page,
            methods=["GET"]
        )

        # Create User Account
        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=CreateUserAccountController.as_view(
                "create_user_account",
                self.create_account_boundary,
                self.user_account
            ),
            methods=["POST"]
        )

        # View User Account
        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>",
            view_func=ViewUserAccountController.as_view(
                "view_user_account",
                self.view_account_boundary,
                self.user_account
            ),
            methods=["GET"]
        )

        # Update User Account
        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/edit",
            view_func=UpdateUserAccountController.as_view(
                "update_user_account",
                self.update_account_boundary,
                self.user_account
            ),
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate User Account
        self.app.add_url_rule(
            "/user-admin/accounts/<int:account_id>/status",
            view_func=SuspendUserAccountController.as_view(
                "suspend_user_account",
                self.suspend_account_boundary,
                self.user_account
            ),
            methods=["POST"]
        )

        # View User Profiles listing
        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=UserProfilesController.as_view(
                "user_profiles",
                self.profiles_boundary,
                self.user_profile
            ),
            methods=["GET"]
        )

        # Display Create User Profile page
        self.app.add_url_rule(
            "/user-admin/profiles/create",
            endpoint="create_user_profile_page",
            view_func=self.create_profile_boundary.display_create_profile_page,
            methods=["GET"]
        )

        # Create User Profile
        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=CreateUserProfileController.as_view(
                "create_user_profile",
                self.create_profile_boundary,
                self.user_profile
            ),
            methods=["POST"]
        )

        # View User Profile
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>",
            view_func=ViewUserProfileController.as_view(
                "view_user_profile",
                self.view_profile_boundary,
                self.user_profile
            ),
            methods=["GET"]
        )

        # Update User Profile
        # Correctly uses the User Profile Boundary
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            view_func=UpdateUserProfileController.as_view(
                "update_user_profile",
                self.update_profile_boundary,
                self.user_profile
            ),
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate User Profile
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/status",
            view_func=SuspendUserProfileController.as_view(
                "suspend_user_profile",
                self.suspend_profile_boundary,
                self.user_profile
            ),
            methods=["POST"]
        )

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
            view_func=CreateCompanyInformationController.as_view(
                "create_company_information",
                self.create_company_boundary,
                self.company_information
            ),
            methods=["POST"]
        )

        # View Company Information
        self.app.add_url_rule(
            "/interior-designer/company",
            view_func=ViewCompanyInformationController.as_view(
                "view_company_information",
                self.view_company_boundary,
                self.company_information
            ),
            methods=["GET"]
        )

        # Update Company Information
        self.app.add_url_rule(
            "/interior-designer/company/edit",
            view_func=UpdateCompanyInformationController.as_view(
                "update_company_information",
                self.update_company_boundary,
                self.company_information
            ),
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate Company Information
        self.app.add_url_rule(
            "/interior-designer/company/status",
            view_func=SuspendCompanyInformationController.as_view(
                "suspend_company_information",
                self.suspend_company_boundary,
                self.company_information
            ),
            methods=["POST"]
        )

        # View all Current IDP and Past IDP projects
        self.app.add_url_rule(
            "/interior-designer/projects",
            view_func=ViewProjectsController.as_view(
                "view_projects",
                self.view_projects_boundary,
                self.project
            ),
            methods=["GET"]
        )

        # Create Current IDP or Past IDP
        self.app.add_url_rule(
            "/interior-designer/projects/create",
            view_func=CreateProjectController.as_view(
                "create_project",
                self.create_project_boundary,
                self.project
            ),
            methods=["GET", "POST"]
        )

        # Search Current IDP and Past IDP projects
        self.app.add_url_rule(
            "/interior-designer/projects/search",
            view_func=SearchProjectController.as_view(
                "search_project",
                self.search_project_boundary,
                self.project
            ),
            methods=["GET"]
        )

        # View an individual Current IDP or Past IDP
        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>",
            view_func=ViewProjectController.as_view(
                "view_project",
                self.view_project_boundary,
                self.project
            ),
            methods=["GET"]
        )

        # Update Current IDP or Past IDP
        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>/edit",
            view_func=UpdateProjectController.as_view(
                "update_project",
                self.update_project_boundary,
                self.project
            ),
            methods=["GET", "POST"]
        )

        # Suspend or Reactivate Current IDP or Past IDP
        self.app.add_url_rule(
            "/interior-designer/projects/<int:project_id>/status",
            view_func=SuspendProjectController.as_view(
                "suspend_project",
                self.suspend_project_boundary,
                self.project
            ),
            methods=["POST"]
        )

    # Run the Flask application
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
