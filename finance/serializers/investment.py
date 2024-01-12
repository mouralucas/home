from base.serializers import CustomSerializer
from rest_framework import serializers


class InvestmentSerializer(CustomSerializer):
    investmentId = serializers.UUIDField(required=True, help_text='The id of the investment')
    investmentName = serializers.CharField(required=True, help_text='The name of the investment')
    date = serializers.DateField(required=True, help_text='The date of the investment')
    maturityDate = serializers.DateField(required=False, help_text='The maturity date of the investment')
    quantity = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, help_text='The quantity of bought of the investment')
    price = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, help_text='The price...')
    amount = serializers.DecimalField(max_digits=15, decimal_places=5, required=True, help_text='The amount acquired')
    cashFlowId = serializers.CharField(max_length=100, required=True, help_text='Incoming ou Outgoing')
    interestRate = serializers.CharField(max_length=100, required=False)
    interestIndex = serializers.CharField(max_length=50, required=False)
    investmentTypeId = serializers.UUIDField(required=True, help_text='The id of the investment type (Treasure bonds, stocks, etc)')
    investmentTypeName = serializers.CharField(max_length=200, required=True, help_text='The name of the investment type')
    custodiaId = serializers.UUIDField(required=True, help_text='The custodian id of the investment')
    custodiaName = serializers.CharField(max_length=100, required=True, help_text='The custodian name of the investment')
    liquidityId = serializers.UUIDField(required=False, help_text='The liquidity id of the investment')
    liquidityName = serializers.CharField(max_length=100, required=False, help_text='The liquidity name of the investment')
    currencyId = serializers.UUIDField(required=False, help_text='The currency id used in the investment')
    currencySymbol = serializers.CharField(max_length=100, required=False, help_text='The currency symbol used in the investment')


class InvestmentTypeSerializer(CustomSerializer):
    investmentTypeId = serializers.UUIDField(required=True)
    investmentTypeName = serializers.CharField(max_length=200, required=True)
    parentId = serializers.UUIDField(required=False)
    parentName = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=600, required=False)
