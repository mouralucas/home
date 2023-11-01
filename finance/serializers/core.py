from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import core.serializers


class ExpenseGetSerializer(core.serializers.CustomSerializer):
    categoryId = serializers.CharField(required=False)
    period = serializers.IntegerField(required=True)
