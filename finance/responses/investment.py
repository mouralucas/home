from base.serializers import CustomSerializer
from base.responses import DefaultSuccessResponse
from rest_framework import serializers


class InvestmentGetResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class InvestmentPostResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class TypeGetResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class StatementGetResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class StatementPostResponse(DefaultSuccessResponse, CustomSerializer):
    pass


class AllocationGetResponse(DefaultSuccessResponse, CustomSerializer):
    pass