from base.serializers import CustomSerializer
from base.responses import DefaultSuccessResponse
from rest_framework import serializers

from finance.serializers.investment import InvestmentTypeSerializer


class InvestmentGetResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class InvestmentPostResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class TypeGetResponse(DefaultSuccessResponse, CustomSerializer):
    quantity = serializers.IntegerField(required=True)
    investmentTypes = InvestmentTypeSerializer(many=True)


class StatementGetResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class StatementPostResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class AllocationGetResponse(DefaultSuccessResponse, CustomSerializer):
    pass
