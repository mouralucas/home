from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class LoginTest(APITestCase):
    def setUp(self):
        self.login_url = '/user/login'
        self.refresh_url = '/user/login/refresh'

        self.username = config('TEST_USER')
        self.password = config('TEST_USER_PASS')

    def test_login(self):
        payload = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


