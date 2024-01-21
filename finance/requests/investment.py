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
    name = serializers.CharField(required=True, help_text='The name of the investment')
    date = serializers.DateField(required=True, help_text='The data that the investment was made')
    quantity = serializers.DecimalField(max_digits=15, decimal_places=5, required=True, help_text='The quantity bought')
    price = serializers.DecimalField(max_digits=15, decimal_places=5, required=True, help_text='The price of the paper')
    amount = serializers.DecimalField(max_digits=15, decimal_places=5, required=True, help_text='The amount of money invested')
    cashFlowId = serializers.CharField(required=True, help_text='The flow of the cash, incoming or outgoing')
    interestRate = serializers.CharField(required=True, help_text='The interest rate of the investment, fixed/floating')
    interestIndex = serializers.CharField(required=True, help_text='The interest index, how much the investment will grow')
    investmentTypeId = serializers.UUIDField(required=True, help_text='The type of investment, e.g bonds, stocks, etc')
    maturityDate = serializers.DateField(required=False, help_text='The maturity date of the investment')
    custodianId = serializers.UUIDField(required=True, help_text='The custodian of the investment')


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
