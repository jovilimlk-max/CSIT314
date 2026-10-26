
'''
What this code does?
- Display the main User Profiles management page.
- Request the list of existing profiles from the Controller.
- Pass the retrieved profiles to the HTML template.
'''

from flask import render_template
from flask.views import MethodView


class UserProfilesPage(MethodView):

    # Receives and stores a reference to the Controller object
    def __init__(self, view_profile_controller):
        self.view_profile_controller = view_profile_controller

    # Retrieve existing profiles and display the management page
    def get(self):
        result, status_code = (
            self.view_profile_controller.get_all_profiles()
        )

        profiles = result["profiles"]

        return render_template(
            "userProfiles.html",
            profiles=profiles
        ), status_code
