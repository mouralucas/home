from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from base.serializers import CustomSerializer


class ReadingGetRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=True)


class ReadingPostRequest(CustomSerializer):
    itemId = serializers.IntegerField(required=True)
    startAt = serializers.DateField(required=True)
    endAt = serializers.DateField(required=False)
    isDropped = serializers.BooleanField(required=False, default=False)


class ProgressGetRequest(CustomSerializer):
    readingId = serializers.UUIDField(required=True)


class ProgressPostRequest(CustomSerializer):
    readingId = serializers.UUIDField(required=True)
    page = serializers.IntegerField(required=False)
    percentage = serializers.IntegerField(required=False, min_value=1, max_value=100)
    rate = serializers.IntegerField(required=False, min_value=0, max_value=5)
    comment = serializers.CharField(required=False)

    def validate(self, data):
        page = data.get('page')
        percentage = data.get('percentage')

        if page is not None and percentage is not None:
            raise ValidationError(_('Ambos \'page\' e \'percentage\' não podem ser fornecidos simultaneamente.'))

        if page is None and percentage is None:
            raise ValidationError(_('Um dos campos \'page\' ou \'percentage\' deve ser fornecido.'))

        return data

