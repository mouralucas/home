import uuid

from decouple import config
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from library.models import Reading, Item


class TestItemReading(APITestCase):
    def setUp(self):
        self.credentials = {
            'username': config('TEST_USER'),
            'password': config('TEST_USER_PASS'),
        }
        self.response = self.client.post('/user/login', data=self.credentials)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.response.data['access']))

        self.url_reading = '/library/item/reading'
        self.url_reading_progress = '/library/reading/progress'
        self.item_id = 100000

        Item.objects.create(
            owner_id='adf52a1e-7a19-11ed-a1eb-0242ac120002',
            id=self.item_id,
            title='Item de teste'
        )

        if self._testMethodName in ['test_set_second_reading_success']:
            self.first_reading_id = uuid.uuid4()
            Reading.objects.create(
                id=self.first_reading_id,
                item_id=self.item_id,
                end_at=timezone.now(),
            )

    def test_set_first_reading_success(self):
        payload = {
            'itemId': self.item_id,
            'startAt': timezone.localdate()
        }
        response = self.client.post(self.url_reading, data=payload)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(response.data['success'])

        self.assertIn('reading', response.data)
        self.assertIn('number', response.data['reading'])
        self.assertEquals(1, response.data['reading']['number'])
        self.assertIn('isDropped', response.data['reading'])
        self.assertFalse(response.data['reading']['isDropped'])

    # def test_set_second_reading_success(self):
    #     payload = {
    #         'itemId': self.item_id,
    #         'startAt': timezone.now()
    #     }
    #     response = self.client.post(self.url, data=payload)
    #
    #     self.assertEquals(status.HTTP_200_OK, response.status_code)
    #     self.assertTrue(response.data['success'])
    #     self.assertIn('reading', response.data)
    #     self.assertIn('number', response.data['reading'])
    #     self.assertEquals(2, response.data['reading']['number'])
    #     self.assertIn('isDropped', response.data['reading'])
    #     self.assertFalse(response.data['reading']['isDropped'])
