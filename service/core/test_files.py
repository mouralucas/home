import os
import tempfile

from rest_framework.test import APITestCase

from service.core.files import Files


class TestFiles(APITestCase):
    def setUp(self):
        csv_content = b"Username;Identifier;First name;Last name\nbooker12;9012;Rachel;Booker"
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.temp_file.write(csv_content)
        self.temp_file.close()

    def test_files_ext(self):
        with self.assertRaises(Exception):
            Files(file='C:/Users/lucas/OneDrive/Financeiro/Rico Investimentos Evolução.xlsx').open_excel(sheet_name='')

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
