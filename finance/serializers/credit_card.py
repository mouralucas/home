from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CreditCardGetSerializer(serializers.Serializer):
    pass

class CreditCardBillGetSerializer(serializers.Serializer):
    bill_id = serializers.IntegerField(required=False)
    period = serializers.IntegerField(required=False)
    card_id = serializers.CharField(required=False)