from rest_framework import serializers


class AccountStatementGetSerializer(serializers.Serializer):
    reference = serializers.IntegerField(required=True)
    accountId = serializers.UUIDField(required=False)


class AccountStatementPostSerializer(serializers.Serializer):
    statementId = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, required=True)
    purchasedAt = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    categoryId = serializers.CharField(required=True)
    accountId = serializers.UUIDField(required=True)
    currencyId = serializers.CharField(required=True)
    cashFlowId = serializers.CharField(required=True)
