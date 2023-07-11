from rest_framework import serializers


class InvestmentGetSerializer(serializers.Serializer):
    investmentId = serializers.UUIDField(required=False)
    showMode = serializers.CharField(required=True)
