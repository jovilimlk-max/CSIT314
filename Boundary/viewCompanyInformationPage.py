
'''
What this code does?
- Display the View Company Information HTML page.
- Retrieve the account ID and username from the URL.
- Validate the account ID.
- Ask the Controller to retrieve the company's information.
- Display existing company information or an empty state.
- Return an error if the account cannot access the page.
'''

from flask import request, render_template
from flask.views import MethodView


class ViewCompanyInformationPage(MethodView):

    # Receive and store a reference to the Controller object
    def __init__(self, view_company_controller):
        self.view_company_controller = view_company_controller

    # Display the Company Information page
    def get(self):

        # Retrieve the account ID from the URL
        account_id = request.args.get("account_id", type=int)

        # Validate the account ID
        if account_id is None or account_id <= 0:
            return "Invalid account ID.", 400

        # Retrieve the username for display
        username = request.args.get(
            "username",
            "Interior Designer"
        ).strip()

        if not username:
            username = "Interior Designer"

        # Ask the Controller to retrieve company information
        result, status_code = (
            self.view_company_controller.view_company_information(
                account_id
            )
        )

        # Return an error if the account is not permitted
        if not result["success"]:
            return result["message"], status_code

        # Display the page with company information
        return render_template(
            "viewCompanyInformation.html",
            account_id=account_id,
            username=username,
            company=result["company"]
        ), 200
