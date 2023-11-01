from rest_framework import status
from rest_framework.test import APITestCase
from decouple import config


class TestAccount(APITestCase):
    def setUp(self):
        user_info = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        response = self.client.post('/user/login', data=user_info)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(response.data['access']))

    def test_get_account(self):
        response = self.client.get('/finance/account')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
