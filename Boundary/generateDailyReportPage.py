
'''
What this code does?
- Handle Daily Report generation requests from Platform Manager.
- Receive the POST request from the Generate button.
- Call the Generate Daily Report Controller.
- Return a JSON success or error response to the frontend.
- Keep HTTP handling and UI messaging in the Boundary.
- Keep report calculations and database operations in the Entity.
'''

from flask import jsonify


class GenerateDailyReportPage:

    # Store the Generate Daily Report Controller
    def __init__(self, generate_daily_report_controller):
        self.controller = generate_daily_report_controller

    # Handle a request to generate a Daily Report
    def post(self):

        # Generate and save the report through the Controller
        result, status_code = self.controller.generate_daily_report()

        # Return the result to the frontend
        return self.display_result(
            result,
            status_code
        )

    # Format the report result as a JSON response
    def display_result(self, result, status_code):

        return jsonify(result), status_code
