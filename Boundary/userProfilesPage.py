
'''
What this code does?
- Display the main User Profiles management page.
- Request the list of existing profiles from the Controller.
- Retrieve the administrator's display name from the URL.
- Pass the profiles and username to the HTML template.
'''

from flask import render_template, request
from flask.views import MethodView


class UserProfilesPage(MethodView):

    # Receive and store a reference to the Controller
    def __init__(self, view_profile_controller):
        self.view_profile_controller = view_profile_controller

    # Retrieve existing profiles and display the management page
    def get(self):
        result, status_code = (
            self.view_profile_controller.get_all_profiles()
        )

        # Return the Controller's error if retrieval fails
        if not result["success"]:
            return result, status_code

        profiles = result["profiles"]

        # Retrieve the logged-in administrator's display name
        username = request.args.get(
            "username", "User Admin"
        ).strip()

        if not username:
            username = "User Admin"

        return render_template(
            "userProfiles.html",
            profiles=profiles,
            username=username
        ), status_code
