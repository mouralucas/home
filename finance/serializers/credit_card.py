from rest_framework import serializers

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
