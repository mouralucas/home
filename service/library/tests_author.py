from django.test import TestCase
from service.library.author import Author


class CreateAuthor(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_get_author(self):
        response = Author().get_author(is_translator=False)

        self.assertTrue(response['success'])
        self.assertEquals(response['length'], len(response['authors']))

    def test_get_translators(self):
        pass

    def test_create_author_success(self):
        pass

    def test_create_author_fail(self):
        pass
