'''
What this code does?
- Entry point for flask
- Initialise flask, connect the BCE classes and register the HTTP routes
'''

from flask import Flask

# Boundaries
from Boundary.userLoginPage import UserLoginPage
from Boundary.userAdminDashboardPage import UserAdminDashboardPage

# Controllers
from Controllers.userLoginController import UserLoginController

# Entities
from Entities.userAccount import UserAccount


class RenovoApp:

    # Initialises Flask, creates the Entity and Controller objects, and registers routes.
    def __init__(self):
        self.app = Flask(__name__, template_folder="FrontEnd")

        # Initialise Entity
        self.user_account = UserAccount()

        # Initialise Controller
        self.login_controller = UserLoginController(
            self.user_account
        )

        # Register application routes
        self.register_routes()

    # Connects the /login URL to the UserLoginPage Boundary class.
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

    # Starts the Flask development server.
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
