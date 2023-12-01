from rest_framework import serializers
from core.serializers import CustomSerializer


class AccountGetSerializer(CustomSerializer):
    accountType = serializers.CharField(required=True)


class StatementGetSerializer(CustomSerializer):
    period = serializers.IntegerField(required=True)
    accountId = serializers.UUIDField(required=False)


class StatementPostSerializer(CustomSerializer):
    statementId = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, required=True)
    purchasedAt = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    categoryId = serializers.CharField(required=True)
    accountId = serializers.UUIDField(required=True)
    currencyId = serializers.CharField(required=True)
    cashFlowId = serializers.CharField(required=True)


class BalanceGetSerializer(CustomSerializer):
    pass


class BalancePostSerializer(serializers.Serializer):
    accountId = serializers.UUIDField(required=True)
