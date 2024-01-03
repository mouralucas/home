from rest_framework import serializers, status

from base.serializers import CustomSerializer
from core.serializers import CategorySerializer


# from base.responses import DefaultSuccessResponse







class CategoryGetResponse(CustomSerializer):
    categories = CategorySerializer(many=True)
