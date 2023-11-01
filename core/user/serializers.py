from rest_framework import serializers
from core.serializers import CustomSerializer


class AccountPostSerializer(CustomSerializer):
    username = serializers.CharField(required=True)
    rawPassword = serializers.CharField(required=True)

