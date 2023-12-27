from rest_framework import serializers

from core.serializers import CustomSerializer


class DefaultSuccessResponse(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    statusCode = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=False)


class DefaultErrorResponse(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    message = serializers.CharField(max_length=250, required=False)
    statusCode = serializers.IntegerField(required=True)


class InvalidTokenError(CustomSerializer, DefaultErrorResponse):
    pass


class InvalidRequestError(CustomSerializer, DefaultErrorResponse):
    errors = serializers.DictField(help_text='A dict with the errors. The key is the error field and the value is the description')
