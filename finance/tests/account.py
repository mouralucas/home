from decouple import config
from rest_framework import status
from rest_framework.test import APITestCase


class TestStatement(APITestCase):
    def setUp(self):
        self.url_statement = '/finance/account/statement'

        user_info = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        response = self.client.post('/user/login', data=user_info)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(response.data['access']))

    def test_get_statement_with_period(self):
        payload = {
            'period': 202301,
        }
        response = self.client.get('/finance/account/statement', payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_statement_with_account_id(self):
        account_id = '16109c7a-0bd5-4ef5-a031-81273299ea9d'
        payload = {
            'accountId': account_id
        }
        response = self.client.get(self.url_statement, data=payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('statementEntry', response.data)
        for i in response.data['statementEntry']:
            self.assertEquals(i['accountId'], account_id)

    def test_post_statement_outgoing(self):
        account_id = 'db8cafdf-b7ac-438c-8f5e-83e769b2fc3c'
        category_id = 'outros'
        amount = 10.15
        purchase_at = '2024-01-03'

        payload = {
            'amount': amount,
            'purchaseAt': purchase_at,
            'description': 'Teste de registro de extrato',
            'categoryId': category_id,
            'accountId': account_id,
            'currencyId': 'BRL',
            'cashFlowId': 'OUTGOING'
        }
        response = self.client.post(self.url_statement, data=payload)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('success', response.data)
        self.assertTrue(response.data['success'])
        self.assertIn('statementEntry', response.data)

        # Assert all required response keys in statementEntry
        self.assertIn('statementEntryId', response.data['statementEntry'])
        self.assertIn('amount', response.data['statementEntry'])
        self.assertIn('accountId', response.data['statementEntry'])
        self.assertIn('accountName', response.data['statementEntry'])
        self.assertIn('categoryId', response.data['statementEntry'])
        self.assertIn('categoryName', response.data['statementEntry'])
        self.assertIn('purchaseAt', response.data['statementEntry'])
        self.assertIn('cashFlowId', response.data['statementEntry'])
        self.assertIn('currencyId', response.data['statementEntry'])
        self.assertIn('currencySymbol', response.data['statementEntry'])

        # Assert if all sent values are returned correctly
        self.assertEquals(float(response.data['statementEntry']['amount']), amount * -1)  # Its outgoing, so multiply by -1 in back-end
        self.assertEquals(response.data['statementEntry']['accountId'], account_id)
        self.assertEquals(response.data['statementEntry']['categoryId'], category_id)
        self.assertEquals(response.data['statementEntry']['purchaseAt'], purchase_at)
        self.assertEquals(response.data['statementEntry']['cashFlowId'], 'OUTGOING')
        self.assertEquals(response.data['statementEntry']['currencyId'], 'BRL')
        self.assertEquals(response.data['statementEntry']['currencySymbol'], 'R$')

    def test_post_statement_missing_param(self):
        response = self.client.post(self.url_statement)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertIn('amount', response.data['errors'])
        self.assertIn('purchaseAt', response.data['errors'])
        self.assertIn('categoryId', response.data['errors'])
        self.assertIn('accountId', response.data['errors'])
        self.assertIn('currencyId', response.data['errors'])
        self.assertIn('cashFlowId', response.data['errors'])

    def tearDown(self):
        pass


class Testa(APITestCase):
    def setUp(self):
        self.url_account = '/finance/account'

        user_info = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        response = self.client.post('/user/login', data=user_info)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(response.data['access']))

    def test_get_account(self):
        response = self.client.get(self.url_account)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_set_account(self):
        bank_id = '989e932e-2217-4f81-baca-14cd4917f214'
        nickname = 'Conta de teste'
        branch = '1489-7'
        account_number = '123489-7'
        open_at = '2024-01-30'
        account_type_id = 1

        payload = {
            'bankId': bank_id,
            'nickname': nickname,
            'description': 'Descrição da conta',
            'branch': branch,
            'accountNumber': account_number,
            'openAt': open_at,
            'accountTypeId': account_type_id
        }
        response = self.client.post(self.url_account, data=payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('account', response.data)
        self.assertIn('accountId', response.data['account'])
        self.assertIn('nickname', response.data['account'])
        self.assertIn('branch', response.data['account'])
        self.assertIn('accountNumber', response.data['account'])
        self.assertIn('openAt', response.data['account'])
        self.assertIn('accountTypeId', response.data['account'])
        self.assertIn('accountTypeName', response.data['account'])

        self.assertEquals(bank_id, response.data['account']['bankId'])
        self.assertEquals(nickname, response.data['account']['nickname'])
        self.assertEquals(account_number, response.data['account']['accountNumber'])
        self.assertEquals(str(open_at), response.data['account']['openAt'])
        self.assertEquals(account_type_id, response.data['account']['accountTypeId'])


def build_requirements(test_name):
    # Functions to populate database with necessary data to test
    # use test_name to create if and don't create unnecessary data slowing down the test
    # call this from setUp()
    pass
