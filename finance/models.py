import uuid
import warnings

from django.db import models
from django.utils.translation import gettext_lazy as _
from numpy import number

import core.models
import finance.choices


class Bank(core.models.Log):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    code = models.SmallIntegerField(null=True)
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'finance"."bank'


class Account(core.models.Log):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bank = models.ForeignKey('finance.Bank', on_delete=models.DO_NOTHING)
    owner = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    nickname = models.CharField(max_length=100, null=True)
    description = models.TextField(_('Descrição da conta'), null=True)
    branch = models.IntegerField(null=True)
    branch_formatted = models.CharField(max_length=30, null=True)
    account_number = models.IntegerField(null=True)
    digit = models.SmallIntegerField(null=True)
    account_number_formatted = models.CharField(max_length=150, null=True)
    dat_open = models.DateField(null=True, help_text=_('Data de início do contrato'))
    dat_close = models.DateField(null=True, help_text=_('Data de fim do contrato'))

    class Meta:
        db_table = 'finance"."account'


# Deprecated
class BankAccount(core.models.Log):
    """
        Essa tabela deve mudar para só contar dados básicos de uma conta bancária/banco (ver como salvar tickets)
        Uma nova tabela Account deve ser criada para lincar user e banco
    """
    id = models.CharField(_('Identificador da conta'), max_length=100, primary_key=True)
    nm_bank = models.CharField(_('Nome da conta'), max_length=150, null=True)
    description = models.TextField(_('Descrição da conta'), null=True)
    branch = models.IntegerField(null=True)
    branch_formatted = models.CharField(max_length=30, null=True)
    account_number = models.IntegerField(null=True)
    digit = models.SmallIntegerField(null=True)
    account_number_formatted = models.CharField(max_length=150, null=True)
    dat_start = models.DateField(null=True, help_text='Data de início do contrato')
    dat_end = models.DateField(null=True, help_text='Data de fim do contrato')
    is_pj = models.BooleanField(default=False, null=True)
    is_debit = models.BooleanField(default=False, null=True, help_text='Indica se a conta tem possibilidade de cartão de débito')
    is_credit = models.BooleanField(default=False, null=True, help_text='Indica se a conta tem possibilidade de cartão de crédito')
    is_investment = models.BooleanField(default=False, help_text='Indica se a conta é para aplicações financeiras')

    class Meta:
        db_table = 'finance"."bank_account'


class CreditCard(core.models.Log):
    id = models.CharField(max_length=100, primary_key=True)
    owner = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    bank_account = models.ForeignKey('finance.BankAccount', on_delete=models.DO_NOTHING, null=True)
    account = models.ForeignKey('finance.Account', on_delete=models.DO_NOTHING, null=True)
    description = models.CharField(max_length=500, null=True)
    dat_start = models.DateField(null=True, help_text=_('Data de início do contrato'))
    dat_end = models.DateField(null=True, help_text=_('Data de fim do contrato'))
    dat_due = models.IntegerField(null=True)
    dat_closing = models.IntegerField(null=True, help_text=_('Data de fechamento da fatura'))

    class Meta:
        db_table = 'finance"."credit_card'


class InvestmentType(core.models.Log):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600, null=True)
    # teste de colunas com texto com idioma dinâmico
    dynamic_name = models.ForeignKey('core.DynamicTextTranslation', on_delete=models.DO_NOTHING, null=True, related_name='finance_investment_type_dynamic_name')
    dynamic_description = models.ForeignKey('core.DynamicTextTranslation', on_delete=models.DO_NOTHING, null=True, related_name='finance_investment_type_dynamic_description')

    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'finance"."investment_type'


class Investment(core.models.Log):
    id = models.UUIDField(max_length=200, primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    type = models.ForeignKey('finance.InvestmentType', on_delete=models.DO_NOTHING)
    date = models.DateField()
    dat_maturity = models.DateField()
    quantity = models.DecimalField(max_digits=15, decimal_places=5, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=5, null=True, help_text=_('Preço do título no momento da compra'))
    amount = models.DecimalField(max_digits=15, decimal_places=5)
    interest_rate = models.CharField(max_length=100, choices=finance.choices.InterestRate.choices)
    interest_index = models.CharField(max_length=50)
    custodian = models.ForeignKey('finance.Bank', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'finance"."investment'


class BankStatement(core.models.Log):
    account_old = models.ForeignKey('finance.BankAccount', on_delete=models.DO_NOTHING, null=True)
    account = models.ForeignKey('finance.Account', on_delete=models.DO_NOTHING, related_name='bank_statement_account')
    owner = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    period = models.IntegerField(null=True, help_text=_('Período de referência'))
    currency = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    amount_absolute = models.DecimalField(max_digits=14, decimal_places=2, help_text=_('O mesmo do amount sem o sinal'))
    dat_purchase = models.DateField(null=True)
    category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)
    cash_flow = models.CharField(max_length=100, choices=finance.choices.CashFlow.choices)

    # Currency exchange fields
    currency_reference = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING, default='BRL', related_name='finance_statement_currency_reference', help_text=_('Moeda de referência'))
    amount_reference = models.DecimalField(max_digits=14, decimal_places=2, default=0, help_text=_('Total na moeda de referência, no caso de câmbio, senão o mesmo valor de amount'))

    dollar_quote = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text=_('Para conta em outras moedas, em relação a moeda de referência'))

    tax = models.DecimalField(max_digits=14, decimal_places=5, default=0, help_text=_('Iof, aplicado sobre a cotação'))
    perc_tax = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text=_('Percentagem do IOF'))
    bank_fee = models.DecimalField(max_digits=14, decimal_places=5, default=0, help_text=_('Spread do banco, aplicado sobre a cotação'))
    perc_bank_fee = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text=_('Percentagem de spread do banco'))
    effective_rate = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text=_('VET: valor efetivo total. valor total do câmbio com as taxas e impostos'))
    # Add compos de porcentagem dos impostos e taxas e no front colocar apenas campo aberto pras porcentagem e calcular na mão
    # Procurar forma de apresentar os valores em reais quando for relacionado a transferência para a conta em dolares, mas manter só o valor quando transação normal e dolar

    # Campos de controle
    origin = models.CharField(max_length=50, default='SYSTEM')
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = 'finance"."bank_statement'


class BankAccountMonthlyBalance(core.models.Log):
    account = models.ForeignKey('finance.BankAccount', on_delete=models.DO_NOTHING)
    period = models.IntegerField(null=True, help_text=_('Período de referência'))
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    earning = models.DecimalField(max_digits=14, decimal_places=2)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = 'finance"."bank_account_monthly_balance'


class CreditCardBill(core.models.Log):
    credit_card = models.ForeignKey('finance.CreditCard', on_delete=models.DO_NOTHING, null=True)
    owner = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    period = models.IntegerField(null=True, help_text=_('Período de referência'))
    dat_payment = models.DateField(null=True)
    dat_purchase = models.DateField(null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, help_text=_('Sempre em reais, valor final na fatura'))
    amount_absolute = models.DecimalField(max_digits=14, decimal_places=2, help_text=_('O mesmo do amount sem o sinal'))
    amount_total = models.DecimalField(max_digits=14, decimal_places=2, help_text=_('Total da compra, quando existe parcelas'))
    category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING, null=True)

    currency = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING)
    amount_currency = models.DecimalField(max_digits=14, decimal_places=2, null=True, help_text=_('Sempre real da compra, na moeda original'))
    price_dollar = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text=_('Usado em compra em outra moeda, em relação ao real'))
    price_currency_dollar = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text=_('Valor da moeda em relação ao dólar, usado na conversão'))
    tax = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text=_('Iof total da compra, quando aplicável'))
    installment = models.SmallIntegerField(default=1)
    tot_installment = models.SmallIntegerField(default=1)
    is_installment = models.BooleanField(default=False)
    father = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)
    cash_flow = models.CharField(max_length=100, choices=finance.choices.CashFlow.choices)

    # Campos de controle
    origin = models.CharField(max_length=50, default='SYSTEM')
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = 'finance"."credit_card_bill'


class CategoryGroup(core.models.Log):
    class GroupType(models.TextChoices):
        FIXED_EXPENSES = ('fixed_expenses', _('Despesas fixas'))
        VARIABLE_EXPENSES = ('variable_expenses', _('Despesas variáveis'))
        NOT_EXPENSE = ('not_expense', _('Não é despesa'))  # Usado para categoria de transferência de valores entre contas

    category = models.ForeignKey('core.Category', on_delete=models.CASCADE, null=True)
    group = models.CharField(max_length=50, choices=GroupType.choices, default=GroupType.VARIABLE_EXPENSES)

    class Meta:
        db_table = 'finance"."category_group'


class Currency(core.models.Log):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    is_shown = models.BooleanField(default=False)

    class Meta:
        db_table = 'finance"."currency'


class CurrencyRate(core.models.Log):
    date = models.DateField()
    base = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_base')
    currency = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_currency')
    price = models.DecimalField(max_digits=30, decimal_places=15)

    class Meta:
        db_table = 'finance"."currency_rate'


##### STOCK MARKET TABLES ######
# class Ticker(core.models.Log):
#     id = models.CharField(max_length=10, primary_key=True)
#     short_name = models.CharField(max_length=200, null=True)
#     long_name = models.CharField(max_length=200, null=True)
#     currency = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING, null=True)
#     logo_url = models.URLField(null=True, help_text='As shown in brapi API')
#
#     class Meta:
#         db_table = 'finance"."ticker'
#
#
# class TikerHistoricalPrice(core.models.Log):
#     date = models.DateField()
#     open = models.DecimalField(max_digits=28, decimal_places=14)
#     high = models.DecimalField(max_digits=28, decimal_places=14)
#     low = models.DecimalField(max_digits=28, decimal_places=14)
#     close = models.DecimalField(max_digits=28, decimal_places=14)
#     volume = models.IntegerField(null=True)
#
#     class Meta:
#         db_table = 'finance"."ticker_historical_price'
#
#
# class PrimeRate(core.models.Log):
#     country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING)
#     date = models.DateField()
#     value = models.DecimalField(max_digits=15, decimal_places=5)
#
#     class Meta:
#         db_table = 'finance"."prime_rate'
