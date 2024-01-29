from rest_framework import serializers

from base.serializers import CustomSerializer
from django.utils.translation import gettext_lazy as _


class CreditCardSerializer(CustomSerializer):
    accountId = serializers.UUIDField(required=False, help_text=_('O id da conta relacionada ao cartão'))
    creditCardId = serializers.CharField(max_length=100, help_text=_('O id do cartão de crédito'))
    nickname = serializers.CharField(max_length=100, help_text=_('Apelido dado pelo usuário ao cartão'))
    description = serializers.CharField(max_length=500, help_text=_('Descrição do cartão de crédito'))
    issuedAt = serializers.DateField(required=False, help_text=_('Data de pedido/emissão do cartão de crédito'))
    cancelledAt = serializers.DateField(required=False, help_text=_('Data de cancelamento do cartão'))
    closingAt = serializers.IntegerField(required=True, help_text=_('Data de fechamento da fatura'))
    dueAt = serializers.IntegerField(required=True, help_text=_('Data de pagamento da fatura'))


class CreditCardBill(CustomSerializer):
    creditCardBillEntryId = serializers.IntegerField(help_text='The id of the bill entry')
    period = serializers.IntegerField(help_text='The period of the purchase')
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, help_text='Tha amount of the purchase')
    purchaseAt = serializers.DateField(help_text='The purchase date')
    paymentAt = serializers.DateField(help_text='The payment date')
    creditCardId = serializers.CharField(max_length=100, help_text='The id of the credit card used in purchase')
    creditCardNickname = serializers.CharField(max_length=100, help_text='The name of the card used in purchase')
    categoryId = serializers.CharField(max_length=200, help_text='The id of purchase category')
    categoryName = serializers.CharField(max_length=200, help_text='The name of the purchase category')
    currencyReferenceId = serializers.CharField(max_length=5, help_text='The id of the currency that was used in purchase')
    currencyReferenceSymbol = serializers.CharField(max_length=5, help_text='The symbol of the currency that was used in purchase')
    installment = serializers.IntegerField(help_text='The installment of the purchase')
    totalInstallment = serializers.IntegerField(help_text='The total installments made')
    createdAt = serializers.DateTimeField(help_text='The date that the entry was created')
    lastEditedAt = serializers.DateTimeField(help_text='The date that the entry was last edited')
    description = serializers.CharField(required=False, help_text='Description of the purchase')
