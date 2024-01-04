from rest_framework import serializers, status

from base.responses import DefaultSuccessResponse
from base.serializers import CustomSerializer
from core.serializers import CategorySerializer, CountrySerializer


# from base.responses import DefaultSuccessResponse


class CategoryGetResponse(DefaultSuccessResponse, CustomSerializer):
    categories = CategorySerializer(many=True)


class CountryPostResponse(DefaultSuccessResponse, CustomSerializer):
    countries = CountrySerializer(many=True)
