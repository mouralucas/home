from django.contrib.auth import authenticate, login, logout

import BO.user.account


class Login(BO.user.account.Account):
    def __init__(self, username=None, raw_password=None, request=None):
        super(Login, self).__init__(username=username, raw_password=raw_password)
        self.request = request

    def authenticate(self):
        """
        :Name: authenticate
        :Created by: Lucas Penha de Moura - 09/06/2022
        :Edited by:

        Check if all data is correct for the user and log the user into the system.
        Create the user session with all information needed to navigate
        """

        # Check if all data is available
        if not self.username or not self.raw_password:
            return {'status': False, 'description': 'All fields are needed', 'redirect': ''}

        # Authenticate the user
        self.user = authenticate(username=self.username, password=self.raw_password)
        if not self.user:
            return {'status': False, 'description': 'User or passwor not found!', 'redirect': ''}

        # Log the user
        login(self.request, self.user)

        # Create the session
        pass

        response = {
            'status': True,
            'redirect': ''
        }

        return response

    def logout(self):
        """
        :Name: logout
        :Created by: Lucas Penha de Moura - 09/06/2022
        :Edited by:

        Log the user out of the system
        """
        logout(self.request)

        response = {
            'status': True,
            'redirect': ''
        }

        return response

    authenticate.__doc__ = 'Used the authenticate a user into the system'
