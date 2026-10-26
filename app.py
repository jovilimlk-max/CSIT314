
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

# Controllers
from Controllers.userLoginController import UserLoginController
from Controllers.createUserAccountController import CreateUserAccountController
from Controllers.createUserProfileController import CreateUserProfileController
from Controllers.viewUserProfileController import ViewUserProfileController
from Controllers.updateUserProfileController import UpdateUserProfileController

# Entities
from Entities.userAccount import UserAccount
from Entities.userProfile import UserProfile


class RenovoApp:

    # Initialise Flask, create the BCE objects and register routes
    def __init__(self):
        self.app = Flask(__name__, template_folder="FrontEnd")

        # Initialise Entities
        self.user_account = UserAccount()
        self.user_account.initialise_database()

        self.user_profile = UserProfile()
        self.user_profile.initialise_database()

        # Initialise Controllers
        self.login_controller = UserLoginController(
            self.user_account,
            self.user_profile
        )

        self.create_account_controller = CreateUserAccountController(
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

        # Register application routes
        self.register_routes()

    # Connect the URLs to their respective Boundary classes
    def register_routes(self):

        # Login Boundary
        login_view = UserLoginPage.as_view(
            "user_login",
            self.login_controller
        )

        # Display login page
        self.app.add_url_rule(
            "/",
            view_func=login_view,
            methods=["GET"]
        )

        # Process login
        self.app.add_url_rule(
            "/login",
            view_func=login_view,
            methods=["POST"]
        )

        # User Admin Dashboard Boundary
        dashboard_view = UserAdminDashboardPage.as_view(
            "user_admin_dashboard"
        )

        # Display User Admin dashboard
        self.app.add_url_rule(
            "/user-admin/dashboard",
            view_func=dashboard_view,
            methods=["GET"]
        )

        # User Accounts Management Boundary
        accounts_view = UserAccountsPage.as_view(
            "user_accounts"
        )

        # Display User Accounts management page
        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=accounts_view,
            methods=["GET"]
        )

        # Create User Account Boundary
        create_account_view = CreateUserAccountPage.as_view(
            "create_user_account",
            self.create_account_controller
        )

        # Display Create User Account page
        self.app.add_url_rule(
            "/user-admin/accounts/create",
            view_func=create_account_view,
            methods=["GET"]
        )

        # Process account creation
        self.app.add_url_rule(
            "/user-admin/accounts",
            view_func=create_account_view,
            methods=["POST"]
        )

        # User Profiles Management Boundary
        profiles_view = UserProfilesPage.as_view(
            "user_profiles",
            self.view_profile_controller
        )

        # Display User Profiles management page
        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=profiles_view,
            methods=["GET"]
        )

        # Create User Profile Boundary
        create_profile_view = CreateUserProfilePage.as_view(
            "create_user_profile",
            self.create_profile_controller
        )

        # Display Create User Profile page
        self.app.add_url_rule(
            "/user-admin/profiles/create",
            view_func=create_profile_view,
            methods=["GET"]
        )

        # Process profile creation
        self.app.add_url_rule(
            "/user-admin/profiles",
            view_func=create_profile_view,
            methods=["POST"]
        )

        # View User Profile Boundary
        view_profile_view = ViewUserProfilePage.as_view(
            "view_user_profile",
            self.view_profile_controller
        )

        # Display the selected user profile
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>",
            view_func=view_profile_view,
            methods=["GET"]
        )

        # Update User Profile Boundary
        update_profile_view = UpdateUserProfilePage.as_view(
            "update_user_profile",
            self.update_profile_controller,
            self.view_profile_controller
        )

        # Display the Update User Profile page
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            view_func=update_profile_view,
            methods=["GET"]
        )

        # Process the profile update
        self.app.add_url_rule(
            "/user-admin/profiles/<int:profile_id>/edit",
            view_func=update_profile_view,
            methods=["POST"]
        )

    # Start the Flask development server
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
