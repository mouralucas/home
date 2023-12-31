from rest_framework import serializers

from core.serializers import CustomSerializer
from util.datetime import DateTime


class AccountGetRequest(CustomSerializer):
    accountType = serializers.CharField(required=True, help_text='Account type (checking, investment, etc)')


class AccountPostRequest(CustomSerializer):
    bank = serializers.UUIDField(required=True, help_text='Id of the bank')
    nickname = serializers.CharField(max_length=100, required=True, help_text='The nickname of the account')
    description = serializers.CharField(max_length=500, required=False, help_text='The description of the account')
    branch = serializers.CharField(max_length=30, required=False, help_text='The branch of the bank')
    account = serializers.CharField(max_length=30, required=False, help_text='The account number')
    openAt = serializers.DateField(required=True, help_text='The date the account was opened')
    closeAt = serializers.DateField(required=False, help_text='The date the account was closed')
    type = serializers.CharField(max_length=150, required=True, help_text='Account type (checking, investment, business, etc)')


class StatementGetRequest(CustomSerializer):
    period = serializers.IntegerField(default=DateTime().current_period(), help_text='The selected period of the statement, default is current period (yyyymm)')
    accountId = serializers.UUIDField(required=False, help_text='The account id of the statement')


class StatementPostRequest(CustomSerializer):
    statementId = serializers.IntegerField(required=False, help_text='The id of the statement')
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, required=True)
    purchaseAt = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    categoryId = serializers.CharField(required=True)
    accountId = serializers.UUIDField(required=True)
    currencyId = serializers.CharField(required=True)
    cashFlowId = serializers.CharField(required=True)


class BalanceGetRequest(CustomSerializer):
    pass


class BalancePostRequest(serializers.Serializer):
    accountId = serializers.UUIDField(required=True)
