from base.serializers import CustomSerializer
from base.responses import DefaultSuccessResponse
from rest_framework import serializers

from library.serializers.reading import ReadingSerializer


class ReadingGetResponse(CustomSerializer, DefaultSuccessResponse):
    readings = ReadingSerializer(many=True, read_only=True)


class ReadingPostResponse(CustomSerializer, DefaultSuccessResponse):
    reading = ReadingSerializer()
