
'''
What this code does?
- Retrieve and validate the Interior Designer's Account ID.
- Retrieve and trim the search query from the URL.
- Validate the search query and its maximum length.
- Allow an empty search query to retrieve all projects.
- Provide validated search details to the Controller.
- Return validation errors as JSON.
- Return matching Current IDP and Past IDP projects as JSON.
- Does not directly communicate with Controllers or Entities.
'''

from flask import request, jsonify


class SearchProjectPage:

    # Retrieve and validate the Interior Designer's Account ID
    def get_account_id(self):

        # Retrieve Account ID from the URL
        account_id = request.args.get(
            "account_id",
            type=int
        )

        # Check that Account ID is a positive integer
        if account_id is None or account_id <= 0:
            return None, {
                "success": False,
                "message": "Invalid account ID."
            }

        return account_id, None

    # Retrieve and validate the search query
    def get_search_query(self):

        # Retrieve search query from URL parameters
        search_query = request.args.get(
            "query",
            default=""
        )

        # Reject invalid search query types
        if not isinstance(search_query, str):
            return None, {
                "success": False,
                "message": "Invalid search query."
            }

        # Remove unnecessary whitespace
        search_query = search_query.strip()

        # Validate the search query length
        if len(search_query) > 255:
            return None, {
                "success": False,
                "message": "Search query cannot exceed 255 characters."
            }

        # Empty search queries are allowed
        # They will retrieve all projects belonging to the company
        return search_query, None

    # Retrieve all validated search information
    def get_search_details(self):

        # Validate Account ID
        account_id, account_error = self.get_account_id()

        if account_error:
            return None, account_error

        # Validate search query
        search_query, query_error = self.get_search_query()

        if query_error:
            return None, query_error

        # Return validated details to the Controller
        return {
            "account_id": account_id,
            "search_query": search_query
        }, None

    # Return input validation errors as JSON
    def display_validation_error(self, error):

        return jsonify(error), 400

    # Return matching projects or an Entity error as JSON
    def display_search_result(self, result, status_code):

        return jsonify(result), status_code
