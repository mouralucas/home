from datetime import timedelta

from decouple import config
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


class TestInvestment(APITestCase):
    def setUp(self):
        self.url_investment = '/finance/investment'

    def test_set_investment_success(self):
        date = timezone.localdate()
        maturity = date + timedelta(days=700)
        quantity = 1.54
        price = 957.35
        amount = quantity * price

        payload = {
            'name': 'Investimento de 29.39% a.m.',
            'date': date,
            'quantity': quantity,
            'price': price,
            'amount': amount,
            'cashFlowId': 'INCOMING',
            'interestRate': '',
            'interestIndex': '',
            'investmentTypeId': '',
            'maturityDate': maturity,
            'custodian': ''
        }
        response = self.client.post(self.url_investment, data=payload)

        # Basic assert
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('success', response.data)
        self.assertTrue(response.data['success'])

        # Assert required responses


class TestInvestmentRelations(APITestCase):
    def setUp(self):
        self.url_investment_account = '/finance/account'
        self.url_investment_type = '/finance/investment/type'

        user_info = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        response = self.client.post('/user/login', data=user_info)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(response.data['access']))

    def test_get_investment_account_success(self):
        # It will not work correctly, account do not filter by type yet
        payload = {
            'accountType': 'True'
        }
        response = self.client.get(self.url_investment_account, data=payload)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data['success'])
        self.assertIn('accounts', response.data)

    def test_get_investment_type_success(self):
        payload = {
            'showMode': 'all'
        }
        response = self.client.get(self.url_investment_type, data=payload)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data['success'])
        self.assertIn('investmentTypes', response.data)

    def test_get_investment_type_fail_payload(self):
        response = self.client.get(self.url_investment_type)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('success', response.data)


class TestInvestmentStatement(APITestCase):
    def setUp(self):
        pass


class TestGoal(APITestCase):
    def setUp(self):
        self.url_goal = '/finance/investment/goal'

    def test_set_goal_success(self):
        payload = {
            'name': 'Comprar uma casa',
            'description': 'Quero uma casa com 6 andares e churrasqueira',
            'targetDate': '2030-01-30'
        }
        response = self.client.post(self.url_goal, data=payload)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        # Assert required values
        self.assertIn('goal', response.data)
        self.assertIn('goalId', response.data['goal'])
        self.assertIn('goalName', response.data['goal'])