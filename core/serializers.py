from base.serializers import CustomSerializer
from rest_framework import serializers


class CategorySerializer(CustomSerializer):
    categoryId = serializers.CharField(max_length=200, required=True, help_text="The category identifier")
    categoryName = serializers.CharField(max_length=250, required=True, help_text="The name of the category")
    description = serializers.CharField(max_length=500, required=False, help_text="The description of the category")
    parentId = serializers.CharField(max_length=200, required=False, help_text="The id of the parent category, if exists")
    parentName = serializers.CharField(max_length=250, required=False, help_text="The name of the parent category, if exists")
    comments = serializers.CharField(required=False, help_text="Comments about the category")
