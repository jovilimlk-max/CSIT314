
'''
What this code does?
- Display the Platform Manager Report landing page.
- Retrieve previously generated reports through the View Reports Controller.
- Display an individual generated report in read-only form.
- Retrieve and validate the Report ID from the URL.
- Handle invalid or missing reports.
- Preserve Platform Manager navigation without Flask sessions.
- Keep HTTP handling and HTML rendering in the Boundary.
- Keep database operations in the Report Entity.
'''

from flask import request, render_template


class ViewReportsPage:

    # Store the View Reports Controller
    def __init__(self, view_reports_controller):
        self.controller = view_reports_controller

    # Retrieve Platform Manager navigation information
    def get_navigation_details(self):

        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        username = request.args.get(
            "username",
            default="Platform Manager"
        ).strip()

        return account_id, username

    # Display the Report landing page
    def get(self):

        account_id, username = self.get_navigation_details()

        # Retrieve all generated reports through the Controller
        reports = self.controller.get_all_reports()

        # Render the Report landing page
        return render_template(
            "viewReports.html",
            account_id=account_id,
            username=username,
            reports=reports
        )

    # Display an individual generated report
    def get_report(self, report_id):

        account_id, username = self.get_navigation_details()

        # Validate Report ID in Boundary
        try:
            report_id = int(report_id)

        except (TypeError, ValueError):
            return "Invalid Report ID.", 400

        if report_id <= 0:
            return "Invalid Report ID.", 400

        # Retrieve the selected report through the Controller
        report = self.controller.get_report_by_id(
            report_id
        )

        # Handle a report that does not exist
        if report is None:
            return "Report not found.", 404

        # Render the read-only report details page
        return render_template(
            "viewReport.html",
            account_id=account_id,
            username=username,
            report=report
        )
