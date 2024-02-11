from base.responses import DefaultSuccessResponse
from base.serializers import CustomSerializer
from core.serializers import CategorySerializer, CountrySerializer, StatusSerializer


class StatusGetResponse(DefaultSuccessResponse, CategorySerializer):
    status = StatusSerializer(many=True, read_only=True)


class CategoryGetResponse(DefaultSuccessResponse, CustomSerializer):
    categories = CategorySerializer(many=True)


class CountryPostResponse(DefaultSuccessResponse, CustomSerializer):
    countries = CountrySerializer(many=True)
