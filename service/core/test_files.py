import os
import tempfile

import pandas as pd
from rest_framework.test import APITestCase

from service.core.files import Files


class TestFiles(APITestCase):
    def setUp(self):
        csv_content_semicolon = b"Username;Identifier;First name;Last name\nbooker12;9012;Rachel;Booker"
        self.temp_file = create_temp_file(csv_content_semicolon)

    def test_file_ext_success(self):
        """
        In this case the test do nothing, the __init__ does not return anything, but validate the ext,
        if pass there is not to be asserted
        """
        try:
            response = Files(self.temp_file.name)
        except Exception as e:
            self.fail('Exception raised: ' + str(e))

    def test_files_ext_fail(self):
        with self.assertRaises(Exception):
            response = Files(file=self.temp_file.name)

    def test_open_csv(self):
        response = Files(self.temp_file.name).open_csv()

        self.assertIsInstance(response, pd.DataFrame)

    def tearDown(self):
        delete_temp_file(self.temp_file.name)


def create_temp_file(file_bytes):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    temp_file.write(file_bytes)
    temp_file.close()

    return temp_file


def delete_temp_file(file):
    if os.path.exists(file):
        os.remove(file)
