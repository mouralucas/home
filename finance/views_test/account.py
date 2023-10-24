from rest_framework.test import APITestCase
from rest_framework import status


class TestAccountViews(APITestCase):

    def setUp(self):
        pass

    def test_account(self):
        user_info = {
            'username': 'lucas',
            'password': 'ezt710sh'
        }
        response = self.client.post('/user/login', data=user_info)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        print(response)
