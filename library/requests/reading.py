from base.serializers import CustomSerializer
from rest_framework import serializers


class ReadingGetRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=True)


class ReadingPostRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=True)
    startAt = serializers.DateField(required=True)
    endAt = serializers.DateField(required=False)
    isDropped = serializers.BooleanField(required=False, default=False)


class ProgressGetRequest(CustomSerializer):
    pass


class ProgressPostRequest(CustomSerializer):
    readingId = serializers.UUIDField(required=True)
    page = serializers.IntegerField(required=False)
    percentage = serializers.IntegerField(required=False, min_value=1, max_value=100)
    rate = serializers.IntegerField(required=False, min_value=0, max_value=5)
    comment = serializers.CharField(required=False)
