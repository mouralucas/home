from rest_framework import serializers

import core.serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class InvestmentGetSerializer(core.serializers.CustomSerializer):
    investmentId = serializers.UUIDField(required=False)
    showMode = serializers.CharField(required=True)

    def validate_showMode(self, value):
        choices = ['all', 'father', 'child']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value


class InvestmentPostSerializer(core.serializers.CustomSerializer):
    parentId = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    quantity = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    price = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    cashFlowId = serializers.CharField(required=True)
    interestRate = serializers.CharField(required=True)
    interestIndex = serializers.CharField(required=True)
    investmentTypeId = serializers.CharField(required=True)
    maturityDate = serializers.DateField(required=False)
    custodianId = serializers.UUIDField(required=True)


class TypeGetSerializer(serializers.Serializer):
    showMode = serializers.CharField(required=True)

    def validate_showMode(self, value):
        choices = ['all', 'father', 'child']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value


class ProfitGetSerializer(core.serializers.CustomSerializer):
    startAt = serializers.IntegerField(required=True)
    investmentId = serializers.UUIDField(required=False)
    referenceId = serializers.UUIDField(required=False, help_text=_('A qual indexador a rentabilidade será comparada'))
