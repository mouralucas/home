import uuid

from decouple import config
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from library.models import Reading, Item, ReadingProgress


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
        self.page_second_entry = 50
        self.page_third_entry = 80

        self.percentage = 10
        self.percentage_second_entry = 25
        self.percentage_third_entry = 90

        if self._testMethodName in ['test_get_progress_success']:
            create_progress(self.reading_id, self.page)
            create_progress(self.reading_id, self.page_second_entry)
            create_progress(self.reading_id, self.page_third_entry)

    def test_set_progress_with_page_success(self):
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

    def test_set_progress_with_percentage_success(self):
        payload = {
            'readingId': self.reading_id,
            'percentage': self.percentage
        }
        response = self.client.post(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('readingProgress', response.data)
        self.assertEquals(str(self.reading_id), response.data['readingProgress']['readingId'])
        self.assertEquals(self.percentage, response.data['readingProgress']['percentage'])
        self.assertEquals(10, response.data['readingProgress']['page'])

    def test_set_progress_without_page_percentage(self):
        payload = {
            'readingId': self.reading_id,
        }
        response = self.client.post(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_set_progress_with_page_percentage(self):
        payload = {
            'readingId': self.reading_id,
        }
        response = self.client.post(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_set_progress_invalid_percentage(self):
        payload = {
            'readingId': self.reading_id,
            'percentage': 105
        }
        response = self.client.post(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_set_progress_invalid_page(self):
        payload = {
            'readingId': self.reading_id,
            'page': 0
        }
        response = self.client.post(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_progress_success(self):
        payload = {
            'readingId': self.reading_id
        }
        response = self.client.get(self.url_reading_progress, data=payload)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('readingProgressEntries', response.data)
        self.assertIsInstance(response.data['readingProgressEntries'], list)
        self.assertIn('quantity', response.data)
        self.assertEquals(3, response.data['quantity'])
        self.assertEquals(str(self.reading_id), response.data['readingProgressEntries'][0]['readingId'])


def create_item(item_id):
    Item.objects.create(
        owner_id='adf52a1e-7a19-11ed-a1eb-0242ac120002',
        id=item_id,
        title='Item de teste',
        pages=100
    )


def create_reading(reading_id, item_id, start_at, end_at=None):
    Reading.objects.create(
        id=reading_id,
        item_id=item_id,
        start_at=start_at,
        end_at=end_at,
    )


def create_progress(reading_id, page):
    tot_pages = 100
    ReadingProgress.objects.create(
        id=uuid.uuid4(),
        reading_id=reading_id,
        date=timezone.now(),
        page=page,
        percentage=(page / tot_pages) * 100
    )
