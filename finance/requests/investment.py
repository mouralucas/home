from rest_framework import serializers

from base.serializers import CustomSerializer
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class InvestmentGetRequest(CustomSerializer):
    investmentId = serializers.UUIDField(required=False)  # Remove and create put/patch endpoint
    showMode = serializers.CharField(required=True)

    def validate_showMode(self, value):
        choices = ['all', 'father', 'child']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value


class InvestmentPostRequest(CustomSerializer):
    name = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    quantity = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    price = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=5, required=True)
    cashFlowId = serializers.CharField(required=True)
    interestRate = serializers.CharField(required=True)
    interestIndex = serializers.CharField(required=True)
    investmentTypeId = serializers.UUIDField(required=True)
    maturityDate = serializers.DateField(required=False)
    custodianId = serializers.UUIDField(required=True)


class TypeGetRequest(CustomSerializer):
    showMode = serializers.CharField(required=True)

    def validate_showMode(self, value):
        choices = ['all', 'father', 'child']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value


class StatementGetRequest(CustomSerializer):
    investmentId = serializers.UUIDField(required=True)
    period = serializers.IntegerField(required=False)


class StatementPostRequest(CustomSerializer):
    investmentId = serializers.UUIDField(required=True)
    period = serializers.IntegerField(required=True)


class ProfitGetRequest(CustomSerializer):
    startAt = serializers.IntegerField(required=True)
    investmentId = serializers.UUIDField(required=False)
    indexId = serializers.UUIDField(required=False, help_text=_('A qual indexador a rentabilidade será comparada'))


class AllocationGetRequest(CustomSerializer):
    # TODO: with the end of father investments, this will be ignores eventually
    showMode = serializers.CharField()

    def validate_showMode(self, value):
        choices = ['father', 'child']
        if value not in choices:
            raise ValidationError(f"O valor '{value}' não é válido. Escolha uma das opções: {', '.join(choices)}.")

        return value
