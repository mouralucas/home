from rest_framework import serializers
from core.serializers import CustomSerializer


class AccountGetSerializer(CustomSerializer):
    accountType = serializers.CharField(required=True, help_text='Account type (checking, investment, etc)')


class StatementGetSerializer(CustomSerializer):
    period = serializers.IntegerField(required=True, help_text='The selected period of the statement')
    accountId = serializers.UUIDField(required=False, help_text='The account id of the statement')


class StatementPostSerializer(CustomSerializer):
    statementId = serializers.IntegerField(required=False, help_text='The id of the statement')
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, required=True)
    purchaseAt = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    categoryId = serializers.CharField(required=True)
    accountId = serializers.UUIDField(required=True)
    currencyId = serializers.CharField(required=True)
    cashFlowId = serializers.CharField(required=True)


class BalanceGetSerializer(CustomSerializer):
    pass


class BalancePostSerializer(serializers.Serializer):
    accountId = serializers.UUIDField(required=True)
