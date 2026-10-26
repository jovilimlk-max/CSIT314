
'''
What this code does?
- Check whether the email is already registered.
- Hash the password before storing it.
- Ask the Entity to create the user account.
- Return the account creation result.
'''

from werkzeug.security import generate_password_hash


class CreateUserAccountController:

    # Stores a reference to the Entity object
    def __init__(self, user_account):
        self.user_account = user_account

    # Coordinate the creation of a new user account
    def create_account(self, account_details):
        name = account_details["name"]
        email = account_details["email"]
        password = account_details["password"]
        role = account_details["role"]

        # Check whether the email is already registered
        existing_user = self.user_account.get_user_by_email(email)

        if existing_user is not None:
            return {
                "success": False,
                "message": "Email address is already registered."
            }, 409

        # Hash the password before storing it
        password_hash = generate_password_hash(password)

        # Ask the Entity to create the account
        created = self.user_account.create_user_account(
            name, email, password_hash, role
        )

        if not created:
            return {
                "success": False,
                "message": "Email address is already registered."
            }, 409

        return {
            "success": True,
            "message": "User account created successfully."
        }, 201
