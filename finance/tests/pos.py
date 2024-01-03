from rest_framework.test import APITestCase


class TestPosStatement(APITestCase):
    def setUp(self):
        self.pagseguro_url = '/pos/import/pag-seguro'

    def test_import_statement_success(self):
        payload = {
            ''
        }
        response = self.client.post(self.pagseguro_url)
