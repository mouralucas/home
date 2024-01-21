from django.db.models import F
from django.utils.translation import gettext_lazy as _
from rest_framework import status

import library.models
from base.responses import DefaultErrorResponse
from library.responses.reading import ReadingPostResponse, ReadingGetResponse
from service.library.library import Library


class Reading(Library):
    def __init__(self, owner, item_id=None):
        super().__init__(owner=owner, item_id=item_id)

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
