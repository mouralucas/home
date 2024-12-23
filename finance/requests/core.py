from rest_framework import serializers

from base.serializers import CustomSerializer


class TransactionByCategoryListGetSerializer(CustomSerializer):
    categoryId = serializers.CharField(required=False)
    period = serializers.IntegerField(required=True)


class TransactionsByCategoryAggregatedGetSerializer(CustomSerializer):
    period = serializers.IntegerField(required=True)


