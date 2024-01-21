from base.serializers import CustomSerializer
from rest_framework import serializers


class ReadingGetRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=True)


class ReadingPostRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=True)
    startAt = serializers.DateField(required=True)
    endAt = serializers.DateField(required=False)
    isDropped = serializers.BooleanField(required=False, default=False)
