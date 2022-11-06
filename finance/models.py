from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models


class BankAccount(core.models.Log):
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
    name = models.CharField(max_length=100)
    bank_account = models.ForeignKey('finance.BankAccount', on_delete=models.DO_NOTHING, null=True)
    description = models.CharField(max_length=500, null=True)
    dat_start = models.DateField(null=True, help_text='Data de início do contrato')
    dat_end = models.DateField(null=True, help_text='Data de fim do contrato')
    dat_due = models.IntegerField(null=True)
    dat_closing = models.IntegerField(null=True, help_text=_('Data de fechamento da fatura'))

    class Meta:
        db_table = 'finance"."credit_card'


class InvestimentType(core.models.Log):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)
    father = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'finance"."investment_type'


class Investment(core.models.Log):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    dat_investment = models.DateField(null=True)
    qtd_titles = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_investment = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Preço do título no momento da compra')
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    profit_contracted = models.CharField(max_length=200, null=True, help_text='Rentabilidade a ser recebida se o título for mantido até o vencimento')

    type = models.ForeignKey('finance.InvestimentType', on_delete=models.DO_NOTHING, null=True)

    maturity = models.DateField(null=True)

    class Meta:
        db_table = 'finance"."investment'


class InvestmentStatement(core.models.Log):
    investment = models.ForeignKey('Investment', on_delete=models.DO_NOTHING, null=True)

    period = models.IntegerField(null=True)
    bank = models.ForeignKey('finance.BankAccount', on_delete=models.DO_NOTHING, null=True)
    gross_profit_annual = models.CharField(max_length=200, null=True, help_text='Taxa equivalente a 1 ano')
    gross_profit = models.CharField(max_length=200, null=True, help_text='Da aplicação até hoje')
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    investment_time = models.IntegerField(null=True, help_text='Dias corridos, contados a partir da data de liquidação do investimento')
    ir_tax_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ir_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    iof_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    b3_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Taxa de custódia da B3')
    bank_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Taxa de custódia da instituição finenceira')
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Valor para resgate antecipado, ou seja, antes do vencimento do título')

    # Campos de controle
    origin = models.CharField(max_length=50, default='SYSTEM')
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = u'"finance\".\"investment_statement"'


class BankStatement(core.models.Log):
    account = models.ForeignKey('finance.BankAccount', on_delete=models.DO_NOTHING)
    reference = models.IntegerField(null=True, help_text='Anomes de referência')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    dat_purchase = models.DateField(null=True)
    category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)

    # Campos de controle
    origin = models.CharField(max_length=50, default='SYSTEM')
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = 'finance"."bank_statement'


class CreditCardBill(core.models.Log):
    credit_card = models.ForeignKey('finance.CreditCard', on_delete=models.DO_NOTHING, null=True)
    reference = models.IntegerField(null=True, help_text=_('Anomes de referência'))
    dat_payment = models.DateField(null=True)
    dat_purchase = models.DateField(null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, help_text=_('Sempre em reais, valor final na fatura'))
    amount_total = models.DecimalField(max_digits=14, decimal_places=2, help_text=_('Total da compra, quando existe parcelas'))
    category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING, null=True)

    currency = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING)
    amount_currency = models.DecimalField(max_digits=14, decimal_places=2, null=True, help_text=_('Sempre real da compra, na moeda original'))
    price_dollar = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text=_('Usado em compra em outra moeda, em relação ao real'))
    price_currency_dollar = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text=_('Valor da moeda em relação ao dolar, usado na conversão'))
    tax = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text=_('Iof total da compra, quando aplicável'))
    installment = models.SmallIntegerField(default=1)
    tot_installment = models.SmallIntegerField(default=1)
    is_stallment = models.BooleanField(default=False)
    father = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)

    # Campos de controle
    origin = models.CharField(max_length=50, default='SYSTEM')
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = 'finance"."creditcard_bill'


class CategoryGroup(core.models.Log):
    class GroupType(models.TextChoices):
        FIXED_EXPENSES = ('fixed_expenses', _('Despesas fixas'))
        VARIABLE_EXPENSES = ('variable_expenses', _('Despesas variáveis'))

    category = models.ForeignKey('core.Category', on_delete=models.CASCADE, null=True)
    group = models.CharField(max_length=50, choices=GroupType.choices, default=GroupType.VARIABLE_EXPENSES)

    class Meta:
        db_table = 'finance"."category_group'


class Currency(core.models.Log):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

    class Meta:
        db_table = 'finance"."currency'


class CurrencyRate(core.models.Log):
    date = models.DateField()
    base = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_base')
    currency = models.ForeignKey('finance.Currency', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_currency')
    price = models.DecimalField(max_digits=30, decimal_places=15)

    class Meta:
        db_table = 'finance"."currency_rate'


class CategoryType(core.models.Log):
    class Type(models.TextChoices):
        INCOMING = ('incoming', _('Entrada'))
        OUTCOMING = 'outcoming', _('Saída')
        INVESTMENT = 'investment', _('Investimentos')

    type = models.CharField(max_length=15, choices=Type.choices)
    category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'finance"."category_type'

