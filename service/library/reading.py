from rest_framework import status

import library.models
from library.responses.reading import ReadingPostResponse
from library.serializers.reading import ReadingSerializer
from service.library.library import Library


class Reading(Library):
    def __init__(self, owner, item_id=None):
        super().__init__(owner=owner, item_id=item_id)

    def set_reading(self, start_at, end_at=None):
        past_readings = library.models.Reading.objects.filter(item_id=self.item_id).order_by('-created_at')

        if past_readings and not past_readings.first().end_at:
            # Add error return that current reading is not done
            return {
                'status': False,
                'statusCOde': status.HTTP_400_BAD_REQUEST
            }

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
                'startAt': new_reading.start_at,
                'endAt': new_reading.end_at,
                'number': new_reading.number,
                'isDropped': new_reading.is_dropped
            }
        }).data

        return response

    def get_reading(self):
        readings = library.models.Reading.objects.filter(item_id=self.item_id)

    def __set_reading_number(self):
        # TODO: read the model filtering by item and owner and count to return number
        pass
