from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase


class TestInvestment(APITestCase):
    def setUp(self):
        self.investment_account_url = '/finance/account'
        self.investment_type_url = '/finance/investment/type'

        user_info = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        response = self.client.post('/user/login', data=user_info)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(response.data['access']))

    def test_get_investment_account_success(self):
        payload = {
            'accountType': 'True'
        }
        response = self.client.get(self.investment_account_url, data=payload)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data['success'])
        self.assertIn('accounts', response.data)

    def test_get_investment_type_success(self):
        payload = {
            'showMode': 'all'
        }
        response = self.client.get(self.investment_type_url, data=payload)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data['success'])
        self.assertIn('investmentTypes', response.data)

    def test_get_investment_type_fail_payload(self):
        response = self.client.get(self.investment_type_url)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
