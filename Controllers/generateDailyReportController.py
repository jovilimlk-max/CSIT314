
'''
What this code does?
- Connect the Generate Daily Report Boundary to the Report Entity.
- Receive a Daily Report generation request from the Boundary.
- Call the Report Entity to generate and save a Daily Report.
- Return the Entity's result to the Boundary.
- Keep HTTP handling and UI messages in the Boundary.
- Keep database operations and calculations in the Entity.
'''


class GenerateDailyReportController:

    # Store the Report Entity
    def __init__(self, report):
        self.report = report

    # Generate a Daily Report through the Entity
    def generate_daily_report(self):

        return self.report.generate_daily_report()
