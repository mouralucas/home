from rest_framework import serializers

from base.serializers import CustomSerializer
from base.responses import DefaultSuccessResponse
from finance.serializers.credit_card import CreditCardSerializer, CreditCardBill


class CreditCardGetResponse(DefaultSuccessResponse, CustomSerializer):
    quantity = serializers.IntegerField(required=True)
    creditCards = CreditCardSerializer(many=True, required=True)


class CreditCardPostResponse(DefaultSuccessResponse, CustomSerializer):
    creditCard = CreditCardSerializer(required=True)


class CreditCardBillGetResponse(DefaultSuccessResponse, CustomSerializer):
    quantity = serializers.IntegerField(required=True)
    billEntries = CreditCardBill(many=True, required=True)


class CreditCardBillPostResponse(CustomSerializer):
    pass
