from rest_framework.test import APITestCase
from rest_framework import status


class TestAccountViews(APITestCase):

    def setUp(self):
        # TODO: criar usuário para cada teste, no tearDown apagar tudo
        user_info = {
            'username': '',
            'password': ''
        }
        response = self.client.post('/user/login', data=user_info)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(response.data['access']))

    def test_account_get(self):
        response = self.client.get('/finance/account')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_account_statement_get(self):
        pass

    def test_account_statement_post(self):
        pass
