
'''
What this code does?
- Handle Monthly Report generation requests from Platform Manager.
- Receive the POST request from the Generate button.
- Call the Generate Monthly Report Controller.
- Return a JSON success or error response to the frontend.
- Keep HTTP handling and UI messaging in the Boundary.
- Keep report calculations and database operations in the Entity.
'''

from flask import jsonify


class GenerateMonthlyReportPage:

    # Store the Generate Monthly Report Controller
    def __init__(self, generate_monthly_report_controller):
        self.controller = generate_monthly_report_controller

    # Handle a request to generate a Monthly Report
    def post(self):

        # Generate and save the report through the Controller
        result, status_code = self.controller.generate_monthly_report()

        # Return the result to the frontend
        return self.display_result(
            result,
            status_code
        )

    # Format the report result as a JSON response
    def display_result(self, result, status_code):

        return jsonify(result), status_code
