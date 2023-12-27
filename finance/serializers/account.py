from core.serializers import CustomSerializer
from rest_framework import serializers


class AccountSerializer(CustomSerializer):
    accountId = serializers.UUIDField(required=True)
    nickname = serializers.CharField(max_length=100)
    branch = serializers.CharField(max_length=30)
    number = serializers.CharField(max_length=150)
    openAt = serializers.DateField()
    closeAt = serializers.DateField()