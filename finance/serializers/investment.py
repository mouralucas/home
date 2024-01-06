from base.serializers import CustomSerializer
from rest_framework import serializers


class InvestmentTypeSerializer(CustomSerializer):
    investmentTypeId = serializers.UUIDField(required=True)
    investmentTypeName = serializers.CharField(max_length=200, required=True)
    parentId = serializers.UUIDField(required=False)
    parentName = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=600, required=False)
