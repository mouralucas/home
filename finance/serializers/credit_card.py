from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import CustomSerializer
from util.datetime import DateTime


class CreditCardGetSerializer(CustomSerializer):
    pass


class CreditCardPostSerializer(CustomSerializer):
    card_number = serializers.CharField()
    # ...


class CreditCardBillGetSerializer(CustomSerializer):
    creditCardBillId = serializers.IntegerField(required=False)
    creditCardId = serializers.CharField(required=False)
    period = serializers.IntegerField(required=False, default=DateTime().current_period())


class CreditCardBillPostSerializer(CustomSerializer):
    creditCardBillId = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(required=True, max_digits=14, decimal_places=2)
    # amountCurrency = serializers.DecimalField(required=False)
    # priceDollar = serializers.DecimalField(required=False)
    # amountTax = serializers.DecimalField(required=False)
    dollarCurrencyQuote = serializers.DecimalField(required=False, max_digits=14, decimal_places=5, default=0)
    purchaseAt = serializers.DateField(required=True)
    paymentAt = serializers.DateField(required=True)
    installment = serializers.IntegerField(required=False, default=1)
    installmentTotal = serializers.IntegerField(required=False, default=1)
    currencyID = serializers.CharField(required=False, default='BRL')
    description = serializers.CharField(required=False)
    categoryId = serializers.UUIDField(required=True)
    creditCardID = serializers.CharField(required=True)
    cashFlowID = serializers.CharField(required=False, default='OUTGOING')


class BillHistorySerializer(CustomSerializer):
    startAt = serializers.IntegerField(required=True)
    endAt = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)

    def validate_type(self, value):
        choices = ['aggregated', 'byCard']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value
