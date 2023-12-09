from rest_framework import status
from rest_framework.test import APITestCase


class TestCore(APITestCase):
    def setUp(self):
        pass

    def test_get_cash_flow(self):
        response = self.client.get('/finance/cash-flow')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('quantity', response.data)
        self.assertGreater(response.data['quantity'], 0)
