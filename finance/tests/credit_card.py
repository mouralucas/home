from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase


class CreditCardTest(APITestCase):
    def setUp(self):
        self.credit_card_url = '/finance/credit-card'
        self.credit_card_bill_url = '/finance/credit-card/bill'

        # All tests are made

        if self._testMethodName not in ['test_get_User_credit_card_without_login']:
            self.credentials = {
                'username': config('TEST_USER'),
                'password': config('TEST_USER_PASS'),
            }
            self.response = self.client.post('/user/login', data=self.credentials)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.response.data['access']))

    def test_get_user_credit_cards_success(self):
        response = self.client.get(self.credit_card_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('creditCards', response.data)
        self.assertIn('creditCards', response.data)
        self.assertIsInstance(response.data['creditCards'], list)

    def test_get_User_credit_card_without_login(self):
        response = self.client.get(self.credit_card_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def create_user_credit_card():
    pass
