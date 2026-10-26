
'''
What this code does?
- Entry point for Flask.
- Initialise Flask and the database.
- Connect the BCE classes and register the HTTP routes.
'''

from flask import Flask

# Boundaries
from Boundary.userLoginPage import UserLoginPage
from Boundary.userAdminDashboardPage import UserAdminDashboardPage
from Boundary.createUserAccountPage import CreateUserAccountPage

# Controllers
from Controllers.userLoginController import UserLoginController
from Controllers.createUserAccountController import CreateUserAccountController

# Entities
from Entities.userAccount import UserAccount


class RenovoApp:

    # Initialise Flask, create the BCE objects and register routes
    def __init__(self):
        self.app = Flask(__name__, template_folder="FrontEnd")

        # Initialise Entity
        self.user_account = UserAccount()
        self.user_account.initialise_database()

        # Initialise Controllers
        self.login_controller = UserLoginController(
            self.user_account
        )

        self.create_account_controller = CreateUserAccountController(
            self.user_account
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

    # Start the Flask development server
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
