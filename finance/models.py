from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models


class BankAccount(core.models.Log):
    id = models.CharField(_('Identificador da conta'), max_length=100, primary_key=True)
    nm_bank = models.CharField(_('Nome da conta'), max_length=150, null=True)
    description = models.TextField(_('Desrição da conta'), null=True)
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
    dat_payment = models.IntegerField(null=True)
    dat_threshold = models.IntegerField(null=True, help_text=_('Data de fechamento da fatura'))

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
    price_investiment = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Preço do título no momento da compra')
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    profit_contracted = models.CharField(max_length=200, null=True, help_text='Rentabilidade a ser recebida se o título for mantido até o vencimento')

    type = models.ForeignKey('finance.InvestimentType', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'finance"."investment'


class BankStatement(core.models.Log):
    account = models.ForeignKey('finance.BankAccount', on_delete=models.DO_NOTHING)
    reference = models.IntegerField(null=True, help_text='Anomes de referência')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    dat_purchase = models.DateField(null=True)
    category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'finance"."bank_statement'


class CreditCardBill(core.models.Log):
    credit_card = models.ForeignKey('finance.CreditCard', on_delete=models.DO_NOTHING, null=True)
    reference = models.IntegerField(null=True, help_text='Anomes de referência')
    dat_payment = models.DateField(null=True)
    dat_purchase = models.DateField(null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, help_text='Sempre em reais, valor final')
    category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING, null=True)

    currency = models.CharField(max_length=30, choices=core.models.CyrruncyTypes.choices, default=core.models.CyrruncyTypes.REAL)
    amount_currency = models.DecimalField(max_digits=14, decimal_places=2, null=True, help_text='Sempre real da compra, na moeda original')
    price_dollar = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text='Usado em compra em outra moeda, em relação ao real')
    price_currency_dollar = models.DecimalField(max_digits=14, decimal_places=5, null=True, help_text='Valor da moeda em relação ao dolar, usado na conversão')
    tax = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=True, help_text='Iof total da compra, quando aplicável')
    stallment = models.SmallIntegerField(null=True, default=1)
    tot_stallment = models.SmallIntegerField(null=True, default=1)
    is_stallment = models.BooleanField(default=False, null=True)
    father = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)

    # Campos de controle
    origin = models.CharField(max_length=50, default='SISTEMA', null=True)
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = 'finance"."creditcard_bill'


# class ExtratoAplicacao(core.models.Log):
#     aplicacao = models.ForeignKey('Aplicacao', on_delete=models.DO_NOTHING, null=True)
#     referencia = models.IntegerField(null=True)
#     agente_custodia = models.ForeignKey('finance.ContaBancaria', on_delete=models.DO_NOTHING, null=True)
#     tipo_aplicacao = models.CharField(max_length=200, default='Tesouro direto')
#     dat_aplicacao = models.DateField(null=True)
#     qtd_titulos = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     preco_aplicacao = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Preço do título no momento da compra')
#     vlr_investido = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     rent_contratada = models.CharField(max_length=200, null=True, help_text='Rentabilidade a ser recebida se o título for mantido até o vencimento')
#     rent_bruta_acum_anual = models.CharField(max_length=200, null=True, help_text='Taxa equivalente a 1 ano')
#     rent_bruta_acum = models.CharField(max_length=200, null=True, help_text='Da aplicação até hoje')
#     vlr_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     tempo_aplicacao = models.IntegerField(null=True, help_text='Dias corridos, contados a partir da data de liquidação do investimento')
#     aliquota_ir = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     imposto_previsto_ir = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     imposto_previsto_iof = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     taxa_b3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Taxa de custódia da B3')
#     taxa_inst_financeira = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Taxa de custódia da instituição finenceira')
#     vlr_liquido = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='Valor para resgate antecipado, ou seja, antes do vencimento do título')
#     vencimento = models.DateField(null=True)
#
#     class Meta:
#         db_table = u'"finance\".\"extrato_investimento"'

class CategoryGroup(core.models.Log):
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE, null=True)
    group = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'finance"."category_group'
