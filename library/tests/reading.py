import uuid

from decouple import config
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from library.models import Reading, Item


class TestReading(APITestCase):
    def setUp(self):
        self.credentials = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        self.response = self.client.post('/user/login', data=self.credentials)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.response.data['access']))

        self.url_reading = '/library/item/reading'
        self.item_id = 100000

        self.first_reading_id = uuid.uuid4()

        create_item(self.item_id)

        if self._testMethodName in ['test_set_second_reading_success', 'test_get_reading_success']:
            start_at = timezone.now() - timezone.timedelta(days=120)
            end_at = timezone.now() - timezone.timedelta(days=60)
            create_reading(reading_id=self.first_reading_id, item_id=self.item_id, start_at=start_at, end_at=end_at)

        if self._testMethodName in ['test_set_second_reading_fail']:
            start_at = timezone.now() - timezone.timedelta(days=15)
            create_reading(self.first_reading_id, item_id=self.item_id, start_at=start_at)

    def test_set_first_reading_success(self):
        payload = {
            'itemId': self.item_id,
            'startAt': timezone.localdate()
        }
        response = self.client.post(self.url_reading, data=payload)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('reading', response.data)
        self.assertIn('readingNumber', response.data['reading'])
        self.assertEquals(1, response.data['reading']['readingNumber'])
        self.assertIn('isDropped', response.data['reading'])
        self.assertFalse(response.data['reading']['isDropped'])

    def test_set_second_reading_success(self):
        payload = {
            'itemId': self.item_id,
            'startAt': timezone.localdate()
        }
        response = self.client.post(self.url_reading, data=payload)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('reading', response.data)
        self.assertIn('readingNumber', response.data['reading'])
        self.assertEquals(2, response.data['reading']['readingNumber'])
        self.assertIn('isDropped', response.data['reading'])
        self.assertFalse(response.data['reading']['isDropped'])

    def test_set_second_reading_fail(self):
        payload = {
            'itemId': self.item_id,
            'startAt': timezone.localdate()
        }
        response = self.client.post(self.url_reading, data=payload)

        self.assertEquals(status.HTTP_409_CONFLICT, response.status_code)
        self.assertFalse(response.data['success'])

    def test_get_reading_success(self):
        payload = {
            'itemId': self.item_id
        }
        response = self.client.get(self.url_reading, data=payload)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('readings', response.data)
        self.assertIsInstance(response.data['readings'], list)


class TestReadingProgress(APITestCase):
    def setUp(self):
        self.credentials = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        self.response = self.client.post('/user/login', data=self.credentials)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.response.data['access']))

        self.url_reading_progress = '/library/item/reading/progress'

        self.item_id = 100000
        self.reading_id = uuid.uuid4()

        create_item(item_id=self.item_id)
        create_reading(reading_id=self.reading_id, item_id=self.item_id, start_at=timezone.now())

        self.page = 32

    def test_set_progress_success(self):
        payload = {
            'readingId': self.reading_id,
            'page': self.page
        }
        response = self.client.post(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('readingProgress', response.data)
        self.assertEquals(str(self.reading_id), response.data['readingProgress']['readingId'])
        self.assertEquals(self.page, response.data['readingProgress']['page'])

    def test_set_progress_fail(self):
        payload = {
            'readingId': self.reading_id,
        }
        response = self.client.post(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)


def create_item(item_id):
    Item.objects.create(
        owner_id='adf52a1e-7a19-11ed-a1eb-0242ac120002',
        id=item_id,
        title='Item de teste'
    )


def create_reading(reading_id, item_id, start_at, end_at=None):
    Reading.objects.create(
        id=reading_id,
        item_id=item_id,
        start_at=start_at,
        end_at=end_at,
    )
