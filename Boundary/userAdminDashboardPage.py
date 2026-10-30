
from flask import render_template
from flask.views import MethodView


class UserAdminDashboardPage(MethodView):

    def get(self):
        return render_template("userAdminDashboard.html")
