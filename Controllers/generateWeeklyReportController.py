
'''
What this code does?
- Connect the Generate Weekly Report Boundary to the Report Entity.
- Receive a Weekly Report generation request from the Boundary.
- Call the Report Entity to generate and save a Weekly Report.
- Return the Entity's result to the Boundary.
- Keep HTTP handling and UI messages in the Boundary.
- Keep report calculations and database operations in the Entity.
'''


class GenerateWeeklyReportController:

    # Store the Report Entity
    def __init__(self, report):
        self.report = report

    # Generate a Weekly Report through the Entity
    def generate_weekly_report(self):

        return self.report.generate_weekly_report()
