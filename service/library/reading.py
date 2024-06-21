from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status

import library.models
from base.responses import DefaultErrorResponse
from library.models import (Reading as ReadingModel, ReadingProgress as ReadingProgressModel)
from library.responses.reading import ReadingPostResponse, ReadingGetResponse, ProgressPostResponse, ProgressGetResponse
from service.library.library import Library


class Reading(Library):
    def __init__(self, owner, item_id=None, request=None):
        super().__init__(owner=owner, item_id=item_id, request=request)

    def get_reading(self):
        readings = (library.models.Reading.objects.annotate(
            readingId=F('pk'),
            itemId=F('item_id'),
            itemTitle=F('item__title'),
            startAt=F('start_date'),
            endAt=F('finish_date'),
            readingNumber=F('number')
        ).values('readingId', 'itemId', 'itemTitle', 'startAt', 'endAt', 'readingNumber')
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

        if past_readings and not past_readings.first().finish_date:
            # Add error return that current reading is not done
            return DefaultErrorResponse({
                'status': False,
                'statusCode': status.HTTP_409_CONFLICT,
                'message': _('Já existe uma leitura em andamento para este item')
            }).data

        total_readings = past_readings.count()

        new_reading = library.models.Reading(
            owner_id=self.owner,
            item_id=self.item_id,
            start_date=start_at,
            finish_date=end_at,
            number=total_readings + 1
        )
        new_reading.save(request_=self.request)

        response = ReadingPostResponse({
            'success': True,
            'statusCode': status.HTTP_201_CREATED,
            'reading': {
                'readingId': new_reading.pk,
                'itemId': new_reading.item_id,
                'itemTitle': new_reading.item.title,
                'startAt': new_reading.start_date,
                'endAt': new_reading.finish_date,
                'readingNumber': new_reading.number,
            }
        }).data

        return response

    def get_progress(self, reading_id):
        entries = (ReadingProgressModel.objects.values('date', 'page', 'percentage', 'rate', 'comment')
                   .annotate(readingProgressEntryId=F('pk'),
                             readingId=F('reading_id')).filter(reading_id=reading_id)).order_by('-date')

        response = ProgressGetResponse({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(entries),
            'readingProgressEntries': entries
        }).data

        return response

    def set_progress(self, reading_id, page=None, percentage=None, rate=None, comment=None):
        # TODO: if the current page = item pages set status to read and set endAt at reading
        # TODO: if a a second progress in add in the same day, only updates the entry, not create another
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
            perc = ((page / item_pages) * 100) if item_pages else 0

            new_progress_entry.page = page
            new_progress_entry.percentage = perc

        if percentage is not None:
            page = (percentage / 100) * item_pages if item_pages else 0
            new_progress_entry.page = int(page)
            new_progress_entry.percentage = percentage

        new_progress_entry.save(request_=self.request)

        response = ProgressPostResponse({
            'success': True,
            'statusCode': status.HTTP_201_CREATED,
            'readingProgress': {
                'readingProgressEntryId': new_progress_entry.pk,
                'readingId': new_progress_entry.reading_id,
                'date': new_progress_entry.date,
                'page': new_progress_entry.page,
                'percentage': new_progress_entry.percentage,
                'rate': new_progress_entry.rate,
                'comment': new_progress_entry.comment
            }
        }).data

        return response
