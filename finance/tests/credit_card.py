from decouple import config
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


class TestCreditCard(APITestCase):
    def setUp(self):
        self.credit_card_url = '/finance/credit-card'

        # All tests are made with the assumption that there is data in database, if not the setUp function must create the necessary inserts
        if self._testMethodName not in ['test_get_user_credit_card_without_login']:
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

        self.assertIn('creditCardId', response.data['creditCards'][0])

    def test_get_user_credit_card_without_login(self):
        response = self.client.get(self.credit_card_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_set_new_user_credit_card(self):
        account_id = '21de1d31-347c-4389-9bd4-70e1b7df2311'
        nickname = 'Cartão novo de teste'
        closing_at = 10
        due_at = 15
        issued_at = timezone.localdate()

        payload = {
            'accountId': account_id,
            'nickname': nickname,
            'description': 'Essa é a descrição deste cartão maroto',
            'issuedAt': issued_at,
            'closingAt': closing_at,
            'dueAt': due_at
        }
        response = self.client.post(self.credit_card_url, data=payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('creditCard', response.data)
        self.assertIn('creditCardId', response.data['creditCard'])
        self.assertIn('closingAt', response.data['creditCard'])
        self.assertIn('dueAt', response.data['creditCard'])

        self.assertEqual(account_id, response.data['creditCard']['accountId'])
        self.assertEqual(nickname, response.data['creditCard']['nickname'])
        self.assertEqual(closing_at, response.data['creditCard']['closingAt'])
        self.assertEqual(due_at, response.data['creditCard']['dueAt'])
        self.assertEqual(str(issued_at), response.data['creditCard']['issuedAt'])


class TestCreditCardBill(APITestCase):
    def setUp(self):
        self.credit_card_bill_url = '/finance/credit-card/bill'

        if self._testMethodName not in ['test_credit_card_bill_get_without_login']:
            self.credentials = {
                'username': config('TEST_USER'),
                'password': config('TEST_USER_PASS'),
            }
            self.response = self.client.post('/user/login', data=self.credentials)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.response.data['access']))

    def test_credit_card_bill_get_success(self):
        pass

    def test_credit_card_bill_get_without_login(self):
        response = self.client.get(self.credit_card_bill_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_credit_card_bill_set_success(self):
        pass
