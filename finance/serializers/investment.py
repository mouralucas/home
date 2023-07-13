from rest_framework import serializers


class InvestmentGetSerializer(serializers.Serializer):
    investmentId = serializers.UUIDField(required=False)
    showMode = serializers.CharField(required=True)


class InvestmentPostSerializer(serializers.Serializer):
    parentId = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    quantity = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    price = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    cashFlowId = serializers.CharField(required=True)
    interestRate = serializers.CharField(required=True)
    interestIndex = serializers.CharField(required=True)
    investmentTypeId = serializers.CharField(required=True)
    maturityDate = serializers.DateField(required=False)
    custodianId = serializers.UUIDField(required=True)