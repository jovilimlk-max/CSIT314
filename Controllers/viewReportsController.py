
'''
What this code does?
- Connect the View Reports Boundary to the Report Entity.
- Retrieve all generated reports for the Platform Manager Report page.
- Retrieve an individual report using its validated Report ID.
- Return the Entity's results to the Boundary.
- Keep HTTP handling, input validation and HTML rendering in Boundary.
- Keep database operations in Entity.
'''


class ViewReportsController:

    # Store the Report Entity
    def __init__(self, report):
        self.report = report

    # Retrieve all generated reports
    def get_all_reports(self):

        return self.report.get_all_reports()

    # Retrieve a specific generated report
    def get_report_by_id(self, report_id):

        return self.report.get_report_by_id(
            report_id
        )
