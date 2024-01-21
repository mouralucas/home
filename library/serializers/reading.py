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
