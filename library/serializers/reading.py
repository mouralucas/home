from base.serializers import CustomSerializer
from rest_framework import serializers


class ReadingSerializer(CustomSerializer):
    readingId = serializers.UUIDField(required=True)
    itemId = serializers.IntegerField(required=True)
    startAt = serializers.DateField(required=True)
    endAt = serializers.DateField(required=False)
    number = serializers.IntegerField(required=True)
    isDropped = serializers.BooleanField(required=False)
