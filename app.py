
'''
What this code does?
- Initialise Flask and all Renovo databases.
- Connect User Admin, Interior Designer, Customer and Platform Manager BCE classes.
- Register Login, User Account and User Profile routes.
- Register Interior Designer Company Information and Project routes.
- Register Customer Project, Save/Unsave and Saved List routes.
- Register Platform Manager IDP Category management routes.
- Register Daily, Weekly and Monthly Report generation routes.
- Register generated Report listing and individual Report viewing routes.
- Store generated reports in the separate Database/report.db.
- Preserve the Boundary -> Controller -> Entity -> Controller -> Boundary flow.
- Do not use Flask sessions or SECRET_KEY.
'''

from flask import Flask

# User Admin Boundaries
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

# Interior Designer Boundaries
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

# Customer Boundaries
from Boundary.customerSearchProjectPage import CustomerSearchProjectPage
from Boundary.customerViewProjectPage import CustomerViewProjectPage
from Boundary.customerSaveProjectPage import CustomerSaveProjectPage
from Boundary.customerSavedProjectsPage import CustomerSavedProjectsPage
from Boundary.customerViewCompanyPage import CustomerViewCompanyPage

# Platform Manager IDP Category Boundaries
from Boundary.createIDPCategoryPage import CreateIDPCategoryPage
from Boundary.viewIDPCategoriesPage import ViewIDPCategoriesPage
from Boundary.viewIDPCategoryPage import ViewIDPCategoryPage
from Boundary.updateIDPCategoryPage import UpdateIDPCategoryPage
from Boundary.suspendIDPCategoryPage import SuspendIDPCategoryPage

# Platform Manager Report Boundaries
from Boundary.generateDailyReportPage import GenerateDailyReportPage
from Boundary.generateWeeklyReportPage import GenerateWeeklyReportPage
from Boundary.generateMonthlyReportPage import GenerateMonthlyReportPage
from Boundary.viewReportsPage import ViewReportsPage

# User Admin Controllers
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

# Interior Designer Controllers
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

# Customer Controllers
from Controllers.customerSearchProjectController import CustomerSearchProjectController
from Controllers.customerViewProjectController import CustomerViewProjectController
from Controllers.customerSaveProjectController import CustomerSaveProjectController
from Controllers.customerSavedProjectsController import CustomerSavedProjectsController
from Controllers.customerViewCompanyController import CustomerViewCompanyController

# Platform Manager IDP Category Controllers
from Controllers.createIDPCategoryController import CreateIDPCategoryController
from Controllers.viewIDPCategoriesController import ViewIDPCategoriesController
from Controllers.viewIDPCategoryController import ViewIDPCategoryController
from Controllers.updateIDPCategoryController import UpdateIDPCategoryController
from Controllers.suspendIDPCategoryController import SuspendIDPCategoryController

# Platform Manager Report Controllers
from Controllers.generateDailyReportController import GenerateDailyReportController
from Controllers.generateWeeklyReportController import GenerateWeeklyReportController
from Controllers.generateMonthlyReportController import GenerateMonthlyReportController
from Controllers.viewReportsController import ViewReportsController

# Entities
from Entities.userAccount import UserAccount
from Entities.userProfile import UserProfile
from Entities.companyInformation import CompanyInformation
from Entities.project import Project
from Entities.savedProject import SavedProject
from Entities.idpCategory import IDPCategory
from Entities.report import Report


class RenovoApp:

    # Initialise Flask, Entities, Controllers and Boundaries
    def __init__(self):

        self.app = Flask(
            __name__,
            template_folder="FrontEnd"
        )

        # Initialise User Admin Entities
        self.user_account = UserAccount()
        self.user_account.initialise_database()

        self.user_profile = UserProfile()
        self.user_profile.initialise_database()

        # Initialise Interior Designer Entities
        self.company_information = CompanyInformation()
        self.company_information.initialise_database()

        self.idp_category = IDPCategory()
        self.idp_category.initialise_database()

        self.project = Project()
        self.project.initialise_database()

        # Initialise Customer Saved Projects Entity
        self.saved_project = SavedProject()
        self.saved_project.initialise_database()

        # Initialise Platform Manager Report Entity
        self.report = Report()
        self.report.initialise_database()

        # Shared Login Controller and Boundary
        self.login_controller = UserLoginController(
            self.user_account
        )

        self.login_boundary = UserLoginPage(
            self.login_controller
        )

        # User Admin Controllers
        self.dashboard_controller = UserAdminDashboardController(
            self.user_account
        )

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

        # User Admin Boundaries
        self.dashboard_boundary = UserAdminDashboardPage(
            self.dashboard_controller
        )

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

        # Interior Designer Controllers
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

        # Interior Designer Boundaries
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

        # Customer Controllers
        self.customer_search_project_controller = CustomerSearchProjectController(
            self.project
        )

        self.customer_view_project_controller = CustomerViewProjectController(
            self.project
        )

        self.customer_save_project_controller = CustomerSaveProjectController(
            self.saved_project
        )

        self.customer_saved_projects_controller = CustomerSavedProjectsController(
            self.saved_project
        )

        self.customer_view_company_controller = CustomerViewCompanyController(
            self.project
        )

        # Customer Boundaries
        self.customer_search_project_boundary = CustomerSearchProjectPage(
            self.customer_search_project_controller
        )

        self.customer_view_project_boundary = CustomerViewProjectPage(
            self.customer_view_project_controller
        )

        self.customer_save_project_boundary = CustomerSaveProjectPage(
            self.customer_save_project_controller
        )

        self.customer_saved_projects_boundary = CustomerSavedProjectsPage(
            self.customer_saved_projects_controller
        )

        self.customer_view_company_boundary = CustomerViewCompanyPage(
            self.customer_view_company_controller
        )

        # Platform Manager IDP Category Controllers
        self.create_idp_category_controller = CreateIDPCategoryController(
            self.idp_category
        )

        self.view_idp_categories_controller = ViewIDPCategoriesController(
            self.idp_category
        )

        self.view_idp_category_controller = ViewIDPCategoryController(
            self.idp_category
        )

        self.update_idp_category_controller = UpdateIDPCategoryController(
            self.idp_category
        )

        self.suspend_idp_category_controller = SuspendIDPCategoryController(
            self.idp_category
        )

        # Platform Manager IDP Category Boundaries
        self.create_idp_category_boundary = CreateIDPCategoryPage(
            self.create_idp_category_controller
        )

        self.view_idp_categories_boundary = ViewIDPCategoriesPage(
            self.view_idp_categories_controller
        )

        self.view_idp_category_boundary = ViewIDPCategoryPage(
            self.view_idp_category_controller
        )

        self.update_idp_category_boundary = UpdateIDPCategoryPage(
            self.update_idp_category_controller
        )

        self.suspend_idp_category_boundary = SuspendIDPCategoryPage(
            self.suspend_idp_category_controller
        )

        # Platform Manager Report Controllers
        self.generate_daily_report_controller = GenerateDailyReportController(
            self.report
        )

        self.generate_weekly_report_controller = GenerateWeeklyReportController(
            self.report
        )

        self.generate_monthly_report_controller = GenerateMonthlyReportController(
            self.report
        )

        self.view_reports_controller = ViewReportsController(
            self.report
        )

        # Platform Manager Report Boundaries
        self.generate_daily_report_boundary = GenerateDailyReportPage(
            self.generate_daily_report_controller
        )

        self.generate_weekly_report_boundary = GenerateWeeklyReportPage(
            self.generate_weekly_report_controller
        )

        self.generate_monthly_report_boundary = GenerateMonthlyReportPage(
            self.generate_monthly_report_controller
        )

        self.view_reports_boundary = ViewReportsPage(
            self.view_reports_controller
        )

        # Register all HTTP routes
        self.register_routes()

    # Register each route directly with its Boundary
    def register_routes(self):

        # Helper for registering one HTTP method per endpoint
        def route(url, endpoint, method, handler):

            self.app.add_url_rule(
                url,
                endpoint=endpoint,
                view_func=handler,
                methods=[method]
            )

        # -------------------------------------------------
        # Shared Login
        # -------------------------------------------------

        route(
            "/",
            "user_login_page",
            "GET",
            self.login_boundary.display_login_page
        )

        route(
            "/login",
            "user_login",
            "POST",
            self.login_boundary.post
        )

        # -------------------------------------------------
        # User Admin Dashboard
        # -------------------------------------------------

        route(
            "/user-admin/dashboard",
            "user_admin_dashboard",
            "GET",
            self.dashboard_boundary.get
        )

        # -------------------------------------------------
        # User Accounts
        # -------------------------------------------------

        route(
            "/user-admin/accounts",
            "user_accounts",
            "GET",
            self.accounts_boundary.get
        )

        route(
            "/user-admin/accounts/create",
            "create_user_account_page",
            "GET",
            self.create_account_boundary.display_create_account_page
        )

        route(
            "/user-admin/accounts",
            "create_user_account",
            "POST",
            self.create_account_boundary.post
        )

        route(
            "/user-admin/accounts/<int:account_id>",
            "view_user_account",
            "GET",
            self.view_account_boundary.get
        )

        route(
            "/user-admin/accounts/<int:account_id>/edit",
            "update_user_account_page",
            "GET",
            self.update_account_boundary.get
        )

        route(
            "/user-admin/accounts/<int:account_id>/edit",
            "update_user_account",
            "POST",
            self.update_account_boundary.post
        )

        route(
            "/user-admin/accounts/<int:account_id>/status",
            "suspend_user_account",
            "POST",
            self.suspend_account_boundary.post
        )

        # -------------------------------------------------
        # User Profiles
        # -------------------------------------------------

        route(
            "/user-admin/profiles",
            "user_profiles",
            "GET",
            self.profiles_boundary.get
        )

        route(
            "/user-admin/profiles/create",
            "create_user_profile_page",
            "GET",
            self.create_profile_boundary.display_create_profile_page
        )

        route(
            "/user-admin/profiles",
            "create_user_profile",
            "POST",
            self.create_profile_boundary.post
        )

        route(
            "/user-admin/profiles/<int:profile_id>",
            "view_user_profile",
            "GET",
            self.view_profile_boundary.get
        )

        route(
            "/user-admin/profiles/<int:profile_id>/edit",
            "update_user_profile_page",
            "GET",
            self.update_profile_boundary.get
        )

        route(
            "/user-admin/profiles/<int:profile_id>/edit",
            "update_user_profile",
            "POST",
            self.update_profile_boundary.post
        )

        route(
            "/user-admin/profiles/<int:profile_id>/status",
            "suspend_user_profile",
            "POST",
            self.suspend_profile_boundary.post
        )

        # -------------------------------------------------
        # Interior Designer Company Information
        # -------------------------------------------------

        route(
            "/company/create",
            "create_company_information_page",
            "GET",
            self.create_company_boundary.display_create_company_page
        )

        route(
            "/company/create",
            "create_company_information",
            "POST",
            self.create_company_boundary.post
        )

        route(
            "/interior-designer/company",
            "view_company_information",
            "GET",
            self.view_company_boundary.get
        )

        route(
            "/interior-designer/company/edit",
            "update_company_information_page",
            "GET",
            self.update_company_boundary.get
        )

        route(
            "/interior-designer/company/edit",
            "update_company_information",
            "POST",
            self.update_company_boundary.post
        )

        route(
            "/interior-designer/company/status",
            "suspend_company_information",
            "POST",
            self.suspend_company_boundary.post
        )

        # -------------------------------------------------
        # Interior Designer Projects
        # -------------------------------------------------

        route(
            "/interior-designer/projects",
            "view_projects",
            "GET",
            self.view_projects_boundary.get
        )

        route(
            "/interior-designer/projects/create",
            "create_project_page",
            "GET",
            self.create_project_boundary.get
        )

        route(
            "/interior-designer/projects/create",
            "create_project",
            "POST",
            self.create_project_boundary.post
        )

        route(
            "/interior-designer/projects/search",
            "search_project",
            "GET",
            self.search_project_boundary.get
        )

        route(
            "/interior-designer/projects/<int:project_id>",
            "view_project",
            "GET",
            self.view_project_boundary.get
        )

        route(
            "/interior-designer/projects/<int:project_id>/edit",
            "update_project_page",
            "GET",
            self.update_project_boundary.get
        )

        route(
            "/interior-designer/projects/<int:project_id>/edit",
            "update_project",
            "POST",
            self.update_project_boundary.post
        )

        route(
            "/interior-designer/projects/<int:project_id>/status",
            "suspend_project",
            "POST",
            self.suspend_project_boundary.post
        )

        # -------------------------------------------------
        # Customer Project Browsing
        # -------------------------------------------------

        route(
            "/customer/projects",
            "customer_search_projects",
            "GET",
            self.customer_search_project_boundary.get
        )

        route(
            "/customer/projects/<int:project_id>",
            "customer_view_project",
            "GET",
            self.customer_view_project_boundary.get
        )

        route(
            "/customer/projects/<int:project_id>/company",
            "customer_view_company",
            "GET",
            self.customer_view_company_boundary.get
        )

        # -------------------------------------------------
        # Customer Save / Unsave
        # -------------------------------------------------

        route(
            "/customer/projects/<int:project_id>/save",
            "customer_check_saved_project",
            "GET",
            self.customer_save_project_boundary.get
        )

        route(
            "/customer/projects/<int:project_id>/save",
            "customer_save_project",
            "POST",
            self.customer_save_project_boundary.post
        )

        route(
            "/customer/projects/<int:project_id>/save",
            "customer_unsave_project",
            "DELETE",
            self.customer_save_project_boundary.delete
        )

        route(
            "/customer/saved-projects",
            "customer_saved_projects",
            "GET",
            self.customer_saved_projects_boundary.get
        )

        # -------------------------------------------------
        # Platform Manager IDP Category
        # -------------------------------------------------

        route(
            "/platform-manager/categories",
            "platform_manager_categories",
            "GET",
            self.view_idp_categories_boundary.get
        )

        route(
            "/platform-manager/categories/create",
            "create_idp_category_page",
            "GET",
            self.create_idp_category_boundary.get
        )

        route(
            "/platform-manager/categories/create",
            "create_idp_category",
            "POST",
            self.create_idp_category_boundary.post
        )

        route(
            "/platform-manager/categories/<int:category_id>",
            "view_idp_category",
            "GET",
            self.view_idp_category_boundary.get
        )

        route(
            "/platform-manager/categories/<int:category_id>/edit",
            "update_idp_category_page",
            "GET",
            self.update_idp_category_boundary.get
        )

        route(
            "/platform-manager/categories/<int:category_id>/edit",
            "update_idp_category",
            "POST",
            self.update_idp_category_boundary.post
        )

        route(
            "/platform-manager/categories/<int:category_id>/status",
            "suspend_idp_category",
            "POST",
            self.suspend_idp_category_boundary.post
        )

        # -------------------------------------------------
        # Platform Manager Reports
        # -------------------------------------------------

        # Display the Report landing page
        route(
            "/platform-manager/reports",
            "platform_manager_reports",
            "GET",
            self.view_reports_boundary.get
        )

        # Generate a Daily Report
        route(
            "/platform-manager/reports/daily",
            "generate_daily_report",
            "POST",
            self.generate_daily_report_boundary.post
        )

        # Generate a Weekly Report
        route(
            "/platform-manager/reports/weekly",
            "generate_weekly_report",
            "POST",
            self.generate_weekly_report_boundary.post
        )

        # Generate a Monthly Report
        route(
            "/platform-manager/reports/monthly",
            "generate_monthly_report",
            "POST",
            self.generate_monthly_report_boundary.post
        )

        # View an individual saved Report
        route(
            "/platform-manager/reports/<int:report_id>",
            "view_report",
            "GET",
            self.view_reports_boundary.get_report
        )

    # Start the Flask application
    def run(self):

        self.app.run(debug=True)


if __name__ == "__main__":
    RenovoApp().run()
