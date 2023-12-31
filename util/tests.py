from rest_framework.test import APITestCase
from util import datetime


class TestDateUtil(APITestCase):
    def setUp(self):
        self.valid_period = 202312
        self.invalid_period = 202313

    def test_validate_period_success(self):
        response = datetime.validate_period(self.valid_period)
        self.assertTrue(response)

    def test_validate_period_error(self):
        response = datetime.validate_period(self.invalid_period)
        self.assertFalse(response)

    def test_validate_period_error_with_raise(self):
        with self.assertRaises(ValueError):
            datetime.validate_period(self.invalid_period, raise_exception=True)
