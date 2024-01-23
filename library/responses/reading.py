from base.serializers import CustomSerializer
from base.responses import DefaultSuccessResponse
from rest_framework import serializers

from library.serializers.reading import ReadingSerializer, ProgressSerializer


class ReadingGetResponse(CustomSerializer, DefaultSuccessResponse):
    quantity = serializers.IntegerField(required=True)
    readings = ReadingSerializer(many=True, required=True)


class ReadingPostResponse(CustomSerializer, DefaultSuccessResponse):
    reading = ReadingSerializer(read_only=True)


class ProgressGetResponse(CustomSerializer, DefaultSuccessResponse):
    quantity = serializers.IntegerField(required=True)
    readingProgressEntries = ProgressSerializer(many=True, required=True)


class ProgressPostResponse(CustomSerializer, DefaultSuccessResponse):
    readingProgress = ProgressSerializer(required=True)
