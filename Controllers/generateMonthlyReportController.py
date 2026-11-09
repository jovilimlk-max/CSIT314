
'''
What this code does?
- Connect the Generate Monthly Report Boundary to the Report Entity.
- Receive a Monthly Report generation request from the Boundary.
- Call the Report Entity to generate and save a Monthly Report.
- Return the Entity's result to the Boundary.
- Keep HTTP handling and UI messages in the Boundary.
- Keep report calculations and database operations in the Entity.
'''


class GenerateMonthlyReportController:

    # Store the Report Entity
    def __init__(self, report):
        self.report = report

    # Generate a Monthly Report through the Entity
    def generate_monthly_report(self):

        return self.report.generate_monthly_report()
