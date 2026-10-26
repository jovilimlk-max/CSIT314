
'''
What this code does?
- Display the main User Profiles management page.
- Provide access to the User Profiles section.
- Serve as the Boundary for future profile management features.
'''

from flask import render_template
from flask.views import MethodView


class UserProfilesPage(MethodView):

    # Display the main User Profiles management page
    def get(self):
        return render_template("userProfiles.html")
