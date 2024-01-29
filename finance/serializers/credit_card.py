from rest_framework import serializers

from base.serializers import CustomSerializer


class CreditCardSerializer(CustomSerializer):
    creditCardId = serializers.CharField(max_length=100, help_text='The id of the credit card')
    name = serializers.CharField(max_length=100, help_text='Name of the credit card')
    description = serializers.CharField(max_length=500, help_text='Description of the credit card')
    startAt = serializers.DateField(required=False, help_text='The data that the credit card was requested')
    endAt = serializers.DateField(required=False, help_text='The data that the credit card cancelled')
    closingAt = serializers.IntegerField(required=True, help_text='The closing date')
    dueAt = serializers.IntegerField(required=True, help_text='The due date')


class CreditCardBill(CustomSerializer):
    creditCardBillEntryId = serializers.IntegerField(help_text='The id of the bill entry')
    period = serializers.IntegerField(help_text='The period of the purchase')
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, help_text='Tha amount of the purchase')
    purchaseAt = serializers.DateField(help_text='The purchase date')
    paymentAt = serializers.DateField(help_text='The payment date')
    creditCardId = serializers.CharField(max_length=100, help_text='The id of the credit card used in purchase')
    creditCardName = serializers.CharField(max_length=100, help_text='The name of the card used in purchase')
    categoryId = serializers.CharField(max_length=200, help_text='The id of purchase category')
    categoryName = serializers.CharField(max_length=200, help_text='The name of the purchase category')
    currencyReferenceId = serializers.CharField(max_length=5, help_text='The id of the currency that was used in purchase')
    currencyReferenceSymbol = serializers.CharField(max_length=5, help_text='The symbol of the currency that was used in purchase')
    installment = serializers.IntegerField(help_text='The installment of the purchase')
    totalInstallment = serializers.IntegerField(help_text='The total installments made')
    createdAt = serializers.DateTimeField(help_text='The date that the entry was created')
    lastEditedAt = serializers.DateTimeField(help_text='The date that the entry was last edited')
    description = serializers.CharField(required=False, help_text='Description of the purchase')


