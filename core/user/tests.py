from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class LoginTest(APITestCase):
    def setUp(self):
        self.credentials = {
                'username': config('TEST_USER'),
                'password': config('TEST_USER_PASS'),
            }
        self.response = None

        self.url_with_auth = '/user/test/login/auth'
        self.url_without_auth = '/user/test/login/no-auth'

        self.login_url = '/user/login'
        self.refresh_url = '/user/login/refresh'

        self.username = config('TEST_USER')
        self.password = config('TEST_USER_PASS')

        # Make login for following tests
        if self._testMethodName in ['test_access_token_success', 'test_wrong_token']:
            self.response = self.client.post('/user/login', data=self.credentials)

        # Set the access token in credentials
        if self._testMethodName in ['test_access_token_success']:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.response.data['access']))

        # Set the refresh token in credentials
        if self._testMethodName in ['test_wrong_token']:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.response.data['refresh']))

    def test_login(self):
        payload = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_token_success(self):
        response = self.client.get(self.url_with_auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_wrong_token(self):
        """
        Send the refresh token in the header, must return error
        """
        response = self.client.post(self.url_with_auth)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

