from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status

import library.models
from base.responses import DefaultErrorResponse
from library.models import (Reading as ReadingModel, ReadingProgress as ReadingProgressModel)
from library.responses.reading import ReadingPostResponse, ReadingGetResponse
from service.library.library import Library


class Reading(Library):
    def __init__(self, owner, item_id=None):
        super().__init__(owner=owner, item_id=item_id)

    def get_reading(self):
        readings = (library.models.Reading.objects.annotate(
            readingId=F('pk'),
            itemId=F('item_id'),
            itemTitle=F('item__title'),
            startAt=F('start_at'),
            endAt=F('end_at'),
            readingNumber=F('number'),
            isDropped=F('is_dropped')
        ).values('readingId', 'itemId', 'itemTitle', 'startAt', 'endAt', 'readingNumber', 'isDropped')
                    .filter(item_id=self.item_id)).order_by('number')

        response = ReadingGetResponse({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(readings),
            'readings': readings
        }).data

        return response

    def set_reading(self, start_at, end_at=None):
        past_readings = library.models.Reading.objects.filter(item_id=self.item_id).order_by('-created_at')

        if past_readings and not past_readings.first().end_at:
            # Add error return that current reading is not done
            return DefaultErrorResponse({
                'status': False,
                'statusCode': status.HTTP_409_CONFLICT,
                'message': _('Já existe uma leitura em andamento para este item')
            }).data

        total_readings = past_readings.count()

        new_reading = library.models.Reading.objects.create(
            owner_id=self.owner,
            item_id=self.item_id,
            start_at=start_at,
            end_at=end_at,
            number=total_readings + 1
        )

        response = ReadingPostResponse({
            'success': True,
            'statusCode': status.HTTP_201_CREATED,
            'reading': {
                'readingId': new_reading.pk,
                'itemId': new_reading.item_id,
                'itemTitle': new_reading.item.title,
                'startAt': new_reading.start_at,
                'endAt': new_reading.end_at,
                'readingNumber': new_reading.number,
                'isDropped': new_reading.is_dropped
            }
        }).data

        return response

    def get_progress(self, reading_id):
        pass

    def set_progress(self, reading_id, page=None, percentage=None, rate=None, comment=None):
        reading = ReadingModel.objects.filter(pk=reading_id).first()
        if not reading:
            return DefaultErrorResponse({
                'success': False,
                'message': _('Não foi encontrada uma leitura com essa id'),
                'statusCode': status.HTTP_404_NOT_FOUND
            }).data

        item = reading.item
        item_pages = item.pages

        new_progress_entry = ReadingProgressModel(
            reading=reading,
            date=timezone.localdate(),
            rate=rate,
            comment=comment
        )
        if page is not None:
            perc = ((page/item_pages)*100) if item_pages else 0

            new_progress_entry.page = page
            new_progress_entry.percentage = percentage




