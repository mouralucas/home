from base.serializers import CustomSerializer
from base.responses import DefaultSuccessResponse
from rest_framework import serializers

from library.serializers.reading import ReadingSerializer, ProgressSerializer


class ReadingGetResponse(CustomSerializer, DefaultSuccessResponse):
    quantity = serializers.IntegerField(read_only=True)
    readings = ReadingSerializer(many=True, read_only=True)


class ReadingPostResponse(CustomSerializer, DefaultSuccessResponse):
    reading = ReadingSerializer(read_only=True)


class ProgressPostResponse(CustomSerializer, DefaultSuccessResponse):
    readingProgress = ProgressSerializer(read_only=True)
