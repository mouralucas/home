from rest_framework.exceptions import ValidationError

from core.serializers import CustomSerializer
from rest_framework import serializers


class ReferenceGetRequest(CustomSerializer):
    sMonth = serializers.IntegerField(required=False, min_value=1, max_value=12, default=1)
    sYear = serializers.IntegerField(required=False, default=2018)
    eMonth = serializers.IntegerField(required=False, min_value=1, max_value=12)
    eYear = serializers.IntegerField(required=False)


class CategoryGetRequest(CustomSerializer):
    showMode = serializers.CharField(required=True, help_text='How categories are fetched from the database [all, parent, child]')
    module = serializers.CharField(required=True)

    def validate_showMode(self, value):
        choices = ['all', 'parent', 'child']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value


class CategoryPostRequest(CustomSerializer):
    pass


class StatusGetRequest(CustomSerializer):
    statusType = serializers.CharField(required=True, help_text='Indicate the type os status (reading status, item status, etc)')
