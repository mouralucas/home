from base.serializers import CustomSerializer
from rest_framework import serializers


class AccountSerializer(CustomSerializer):
    accountId = serializers.UUIDField(required=True, help_text='The account identifier')
    nickname = serializers.CharField(max_length=100, help_text='The name of the account, given by the user')
    branch = serializers.CharField(max_length=30, help_text='The branch number of the account')
    number = serializers.CharField(max_length=150, help_text='The number of the account')
    openAt = serializers.DateField(help_text='The date that the account was opened')
    closeAt = serializers.DateField(help_text='The date that the account was closed')


class StatementSerializer(CustomSerializer):
    statementEntryId = serializers.UUIDField(required=True, help_text='The identifier of the statement')
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, required=True, help_text='The amount of the purchase')
    accountName = serializers.CharField(max_length=150, required=True, help_text='The name of the account of the purchase')
    accountId = serializers.UUIDField(required=True, help_text='The identifier of the account')
    categoryName = serializers.CharField(max_length=250, required=True, help_text='The category of the purchase')
    categoryId = serializers.CharField(max_length=200, required=True, help_text='The id of category of the purchase')
    purchaseAt = serializers.DateField(required=True, help_text='Date of the purchase')
    cashFlowId = serializers.CharField(max_length=100, required=True, help_text='The id of the cash flow (incoming or outgoing)')
    currencyId = serializers.CharField(max_length=5, required=True, help_text='The currency identifier with three letters like \'BRL\'')
    currencySymbol = serializers.CharField(max_length=5, required=True, help_text='The currency symbol, like \'R$\'')
    createdAt = serializers.DateTimeField(help_text='Date and time when the register was created')
    lastEditedAt = serializers.DateTimeField(help_text='Date and time when the register was last edited')
    description = serializers.CharField()
