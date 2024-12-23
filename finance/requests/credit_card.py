from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from base.serializers import CustomSerializer
from util import datetime


class CreditCardGetSerializer(CustomSerializer):
    creditCardStatus = serializers.CharField(required=False, default='active')


class CreditCardPostRequest(CustomSerializer):
    nickname = serializers.CharField(max_length=100, required=True)
    accountId = serializers.UUIDField(required=False)
    description = serializers.CharField(required=False)
    issuedAt = serializers.DateField(required=False)
    cancelledAt = serializers.DateField(required=False)
    dueAt = serializers.IntegerField(required=True)
    closingAt = serializers.IntegerField(required=True)


class CreditCardBillGetRequest(CustomSerializer):
    creditCardBillId = serializers.IntegerField(required=False)
    creditCardId = serializers.CharField(required=False)
    period = serializers.IntegerField(required=False, default=datetime.current_period())


class CreditCardBillPostRequest(CustomSerializer):
    creditCardBillId = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(required=True, max_digits=14, decimal_places=2)
    # amountCurrency = requests.DecimalField(required=False)
    # priceDollar = requests.DecimalField(required=False)
    # amountTax = requests.DecimalField(required=False)
    dollarCurrencyQuote = serializers.DecimalField(required=False, max_digits=14, decimal_places=5, default=0)
    purchaseAt = serializers.DateField(required=True)
    paymentAt = serializers.DateField(required=True)
    installment = serializers.IntegerField(required=False, default=1)
    installmentTotal = serializers.IntegerField(required=False, default=1)
    currencyID = serializers.CharField(required=False, default='BRL')
    description = serializers.CharField(required=False)
    categoryId = serializers.CharField(required=True)
    creditCardId = serializers.CharField(required=True)
    cashFlowId = serializers.CharField(required=False, default='OUTGOING')


class BillHistoryRequest(CustomSerializer):
    startAt = serializers.IntegerField(required=True)
    endAt = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)

    def validate_type(self, value):
        choices = ['aggregated', 'byCard']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value
