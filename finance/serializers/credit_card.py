from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import core.serializers


class CreditCardGetSerializer(serializers.Serializer):
    pass


class CreditCardBillGetSerializer(serializers.Serializer):
    bill_id = serializers.IntegerField(required=False)
    period = serializers.IntegerField(required=False)
    card_id = serializers.CharField(required=False)


class BillHistorySerializer(core.serializers.CustomSerializer):
    startAt = serializers.IntegerField(required=True)
    endAt = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)

    def validate_type(self, value):
        choices = ['aggregated', 'byCard']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value
