from rest_framework import serializers

from base.responses import DefaultSuccessResponse
from base.serializers import CustomSerializer
from finance.serializers.investment import InvestmentTypeSerializer, GoalSerializer


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


class GoalGetResponse(DefaultSuccessResponse, CustomSerializer):
    goals = GoalSerializer(many=True, required=True)


class GoalPostResponse(DefaultSuccessResponse, CustomSerializer):
    goal = GoalSerializer(required=True)
