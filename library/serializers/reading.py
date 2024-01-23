from base.serializers import CustomSerializer
from rest_framework import serializers


class ReadingSerializer(CustomSerializer):
    readingId = serializers.UUIDField(required=True)
    itemId = serializers.IntegerField(required=True)
    itemTitle = serializers.CharField(required=True)
    startAt = serializers.DateField(required=True)
    endAt = serializers.DateField(required=False)
    readingNumber = serializers.IntegerField(required=True)
    isDropped = serializers.BooleanField(required=False)


class ProgressSerializer(CustomSerializer):
    readingProgressEntryId = serializers.UUIDField(required=True, help_text='The progress entry identifier')
    readingId = serializers.UUIDField(required=True, help_text='The reading identifier')
    date = serializers.DateField(required=True, help_text='The date that the entry was created')
    page = serializers.IntegerField(required=False, help_text='The page for the current entry')
    percentage = serializers.IntegerField(required=False, help_text='The percentage of the current entry')
    rate = serializers.IntegerField(required=False, help_text='The rate for the current entry')
    comment = serializers.CharField(required=False, help_text='The comment for the current entry')
