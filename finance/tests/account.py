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
        self.assertTrue(response.data['success'])

    def test_get_statement_success(self):
        payload = {
            'period': 202301,
        }
        response = self.client.get('/finance/account/statement', payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_statement_without_payload(self):
        response = self.client.get('/finance/account/statement')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertIn('period', response.data['errors'])

    def test_post_statement(self):
        pass

    def test_post_statement_missing_param(self):
        pass

    def tearDown(self):
        pass
