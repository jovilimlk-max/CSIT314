
'''
What this code does?
- Display the main User Accounts management page.
- Provide access to the User Accounts section.
- Serve as the Boundary for future account management features.
'''

from flask import render_template
from flask.views import MethodView


class UserAccountsPage(MethodView):

    # Display the main User Accounts management page
    def get(self):
        return render_template("userAccounts.html")
