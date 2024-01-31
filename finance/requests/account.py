from rest_framework import serializers

from base.serializers import CustomSerializer
from util import datetime
from django.utils.translation import gettext_lazy as _


class AccountGetRequest(CustomSerializer):
    accountTypeId = serializers.IntegerField(required=True, help_text=_('Tipo da conta, corrente, PJ, investimento, etc'))


class AccountPostRequest(CustomSerializer):
    bankId = serializers.UUIDField(required=True, help_text=_('Id do banco'))
    nickname = serializers.CharField(max_length=100, required=True, help_text=_('Apelido dado a conta pelo usuário'))
    description = serializers.CharField(max_length=500, required=False, help_text=_('Descrição da conta'))
    branch = serializers.CharField(max_length=30, required=False, help_text=_('Número da agência'))
    accountNumber = serializers.CharField(max_length=30, required=False, help_text=_('Número da conta'))
    openAt = serializers.DateField(required=True, help_text=_('Data da abertura da conta'))
    closeAt = serializers.DateField(required=False, help_text=_('Data do encerramento da conta'))
    accountTypeId = serializers.IntegerField(required=True, help_text=_('Tipo da conta, corrente, PJ, investimento, etc'))


class StatementGetRequest(CustomSerializer):
    period = serializers.IntegerField(default=datetime.current_period(), help_text='The selected period of the statement, default is current period (yyyymm)')
    accountId = serializers.UUIDField(required=False, help_text='The account id of the statement')


class StatementPostRequest(CustomSerializer):
    statementId = serializers.IntegerField(required=False, help_text='The id of the statement')  # Change to a PUT ou PATCH
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, required=True)
    purchaseAt = serializers.DateField(required=True)
    description = serializers.CharField(required=False)
    categoryId = serializers.CharField(required=True)
    accountId = serializers.UUIDField(required=True)
    currencyId = serializers.CharField(required=True)
    cashFlowId = serializers.CharField(required=True)


class BalanceGetRequest(CustomSerializer):
    pass


class BalancePostRequest(serializers.Serializer):
    accountId = serializers.UUIDField(required=True)
