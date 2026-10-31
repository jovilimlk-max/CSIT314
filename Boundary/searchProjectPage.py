
'''
What this code does?
- Handle requests to search for projects.
- Retrieve the Interior Designer's account ID.
- Retrieve the search query from the URL.
- Pass the request to SearchProjectController.
- Return matching projects as a JSON response.
'''

from flask import request, jsonify
from flask.views import MethodView


class SearchProjectPage(MethodView):

    # Store a reference to the Controller
    def __init__(self, search_project_controller):
        self.search_project_controller = search_project_controller

    # Handle project search requests
    def get(self):

        # Retrieve the Interior Designer's account ID
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Validate the account ID
        if account_id is None or account_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid account ID."
            }), 400

        # Retrieve the search query
        search_query = request.args.get(
            "query",
            default=""
        )

        # Pass the search request to the Controller
        result, status_code = (
            self.search_project_controller.search_projects(
                account_id,
                search_query
            )
        )

        # Return the Controller's result
        return jsonify(result), status_code
