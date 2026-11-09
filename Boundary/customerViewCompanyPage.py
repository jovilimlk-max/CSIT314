
'''
What this code does?
- Handle Customer requests to view company information for an IDP.
- Validate Customer Account ID and Project ID.
- Retrieve the Customer's display name from the URL.
- Preserve whether the Customer came from IDPs or Saved List.
- Retrieve active company information through the Controller.
- Display company information in a read-only HTML page.
- Mark navigation back to the IDP so it does not count as a new view.
'''

from flask import request, render_template
from urllib.parse import urlencode


class CustomerViewCompanyPage:

    def __init__(self, customer_view_company_controller):
        self.controller = customer_view_company_controller

    # Display company information for the selected IDP
    def get(self, project_id):

        account_id = self.get_account_id()

        if account_id is None:
            return "Invalid or missing Customer Account ID.", 400

        if not isinstance(project_id, int) or project_id <= 0:
            return "Invalid Project ID.", 400

        username = self.get_username()
        source = self.get_source()

        # Retrieve active company information through Controller
        result, status_code = self.controller.view_customer_company(
            project_id
        )

        if not result["success"]:
            return result["message"], status_code

        # Preserve navigation and identify return from Company Information
        parameters = urlencode({
            "account_id": account_id,
            "username": username,
            "source": source,
            "return_from_company": "1"
        })

        back_url = f"/customer/projects/{project_id}?{parameters}"

        # Render Customer Company Information page
        return render_template(
            "customerViewCompany.html",
            company=result["company"],
            project_id=project_id,
            account_id=account_id,
            username=username,
            source=source,
            back_url=back_url
        ), status_code

    # Validate Customer Account ID
    def get_account_id(self):

        account_id = request.args.get(
            "account_id",
            default=""
        ).strip()

        try:
            account_id = int(account_id)
            return account_id if account_id > 0 else None

        except ValueError:
            return None

    # Retrieve Customer display name
    def get_username(self):

        username = request.args.get(
            "username",
            default="Customer"
        ).strip()

        return username or "Customer"

    # Identify original navigation source
    def get_source(self):

        source = request.args.get(
            "source",
            default="idps"
        ).strip().lower()

        return "saved" if source == "saved" else "idps"
