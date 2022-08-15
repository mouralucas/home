import os
from collections import defaultdict
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, F, Case, When, BooleanField, CharField, Value
from django.utils.translation import gettext_lazy as _

import core.models
import core.serializers
import finance.models
import finance.serializers
import util.datetime


class Finance:

    def __init__(self, mes=None, ano=None, statement_id=None, bill_id=None, reference=None, account_id=None, credit_card_id=None, amount=None,
                 amount_currency=None, price_currency_dollar=None, vlr_moeda=None, amount_tax=None, stallment=None, tot_stallment=None, dat_compra=None, dat_pagamento=None,
                 description=None, category_id=None, currency_id=None, price_dollar=None):
        self.mes = mes
        self.ano = ano

        self.statement_id = statement_id
        self.bill_id = bill_id
        self.reference = reference
        self.amount = amount
        self.amount_currency = amount_currency
        self.price_currency_dollar = price_currency_dollar
        self.vlr_moeda = vlr_moeda
        self.amount_tax = amount_tax
        self.stallment = stallment
        self.tot_stallment = tot_stallment
        self.dat_compra = dat_compra
        self.dat_pagamento = dat_pagamento
        self.description = description
        self.categoria_id = category_id
        self.conta_id = account_id
        self.credit_card_id = credit_card_id
        self.currency = currency_id

        self.response = {}

    def get_bank_accounts(self, selected_id=''):
        bank_accounts = finance.models.BankAccount.objects.values('id', 'nm_bank', 'branch_formatted', 'account_number_formatted', 'dat_start',
                                                                  'dat_end').ativos() \
            .annotate(is_selected=Case(When(id=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField()))

        self.response['status'] = True
        self.response['bank_accounts'] = list(bank_accounts)

        return self.response

    def get_credit_cards(self, selected_id=''):
        # TODO: mudar para receber parametro de status
        credit_cards = finance.models.CreditCard.objects.values('id', 'name', 'description', 'dat_threshold', 'dat_payment').ativos() \
            .annotate(nm_status=Case(When(status=True, then=Value('Ativo')),
                                     default=Value('Cancelado'),
                                     output_field=CharField()),
                      is_selected=Case(When(id=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField())).order_by('-status', 'id')

        self.response['status'] = True
        self.response['credit_cards'] = list(credit_cards)

        return self.response

    def get_category(self, selected_id=''):
        categorias = core.models.Category.objects.values('id', 'description', 'comments').ativos() \
            .annotate(is_selected=Case(When(id=selected_id, then=True),
                                       default=False,
                                       output_field=BooleanField()),
                      id_father=F('father_id'),
                      nm_father=F('father__description'))

        self.response['status'] = True
        self.response['categories'] = list(categorias)
        return self.response

    def set_extrato(self, request=None):
        if not self.dat_compra or not self.amount or not self.categoria_id or not self.conta_id:
            self.response['status'] = False
            self.response['descricao'] = 'Todos os parâmetros são obrigatórios'
            return self.response

        if self.statement_id:
            extrato = finance.models.BankStatement.objects.filter(pk=self.statement_id).first()
        else:
            extrato = finance.models.BankStatement()

        # Não modificado nomes
        dat_compra_date = util.datetime.data_to_datetime(self.dat_compra, formato='%d/%m/%Y')
        referencia_ano = dat_compra_date.year
        referencia_mes = dat_compra_date.month
        self.reference = referencia_ano * 100 + referencia_mes

        extrato.reference = self.reference
        extrato.valor = float(self.amount) * -1
        extrato.dat_compra = dat_compra_date
        extrato.descricao = self.description
        extrato.categoria_id = self.categoria_id
        extrato.conta_id = self.conta_id
        extrato.save(request_=request)

    def get_statement(self):
        filters = {
            'reference': self.reference
        }

        if self.conta_id:
            filters['account_id'] = self.conta_id

        statement = finance.models.BankStatement.objects.values('id', 'reference', 'dat_purchase', 'description') \
            .filter(**filters).annotate(total=Sum('amount'),
                                        account=F('account__nm_bank')) \
            .order_by('account_id', 'dat_purchase')

        self.response['status'] = True
        self.response['statement'] = list(statement)
        return self.response

    def set_bill(self, request=None):
        if not self.dat_compra or not self.amount or not self.categoria_id or not self.credit_card_id:
            self.response['status'] = False
            self.response['descricao'] = 'Todos os parâmetros são obrigatórios'
            return self.response

        if self.bill_id:
            bill = finance.models.CreditCardBill.objects.filter(pk=self.bill_id).first()
        else:
            bill = finance.models.CreditCardBill()

        # Não modificado
        dat_pagamento_date = util.datetime.data_to_datetime(self.dat_pagamento, formato='%d/%m/%Y')
        referencia_ano = dat_pagamento_date.year
        referencia_mes = dat_pagamento_date.month
        self.reference = referencia_ano * 100 + referencia_mes

        bill.credit_card_id = self.credit_card_id
        # Dates
        bill.reference = self.reference
        bill.dat_payment = dat_pagamento_date
        bill.dat_purchase = util.datetime.data_to_datetime(self.dat_compra, formato='%d/%m/%Y')

        # Amounts
        bill.amount = float(self.amount) * -1
        bill.amount_total = self.amount  # TODO: modificar para adicionar o valor total de compras parceladas
        bill.amount_currency = float(self.amount_currency) * -1
        bill.price_currency_dollar = self.price_currency_dollar
        bill.price_dollar = 1

        bill.currency = self.currency
        bill.category_id = self.categoria_id

        # bill.stallment = self.nr_parcela
        bill.stallment = 1
        bill.tot_stallment = self.tot_stallment
        bill.description = self.description

        bill.is_validated = True

        bill.save(request_=request)

        response = self.get_bill()

        return response

    def get_bill(self):
        filters = {
            'reference': self.reference
        }

        if self.credit_card_id:
            filters['credit_card_id'] = self.credit_card_id

        faturas = finance.models.CreditCardBill.objects \
            .values('id', 'reference', 'dat_purchase', 'dat_payment',
                    'stallment', 'tot_stallment', 'description') \
            .filter(**filters) \
            .annotate(total=Sum('amount'),
                      card=F('credit_card__name'),
                      nm_category=F('category__description')).order_by('dat_purchase')

        self.response['status'] = True
        self.response['bill'] = list(faturas)

        return self.response

    def get_bill_statistic(self):
        bills = finance.models.CreditCardBill.objects.all()
        qtd_total = bills.count()
        qtd_reference = bills.filter(reference=self.reference).count()

        response = {
            'status': True,
            'qtd_total': qtd_total,
            'qtd_reference': qtd_reference,
        }

        return response

    def get_evolucao_faturas(self, months=13):
        evolucao = finance.models.CreditCardBill.objects.values('reference') \
            .filter(refence__range=(202001, 202112)).annotate(total=Sum('valor'),
                                                              cartao=F('cartao_credito__nm_descritivo')).order_by('reference', 'credit_card_id')

        evolucao = pd.DataFrame(evolucao)
        saida = evolucao.pivot(index='reference', columns='cartao', values='total').fillna(0)

        self.response['status'] = True
        self.response['faturas'] = saida.values.tolist()

        return self.response

    def get_evolucao_categoria(self, months=13):
        fixed_expenses = finance.models.CategoryGroup.objects.values_list('category', flat=True).filter(group='fixed_expenses')
        filters = {
            'reference__range': (202001, 202112),
            'category__in': list(fixed_expenses)
        }

        evolucao_credito = finance.models.CreditCardBill.objects.values('reference', 'category__description') \
            .filter(**filters).annotate(total=Sum('amount')).order_by('reference')

        evolucao_contas = finance.models.BankStatement.objects.values('reference', 'category__description') \
            .filter(**filters).annotate(total=Sum('amount')).order_by('reference')

        evolucao = evolucao_contas.union(evolucao_credito)

        default = defaultdict(float)

        for i in list(evolucao):
            default[str(i.get('reference', '')) + '.' + i.get('category__description', '')] += float(i.get('total', 0))

        default = [{'reference': i.split('.')[0], 'categoria': i.split('.')[1], 'total': default[i]} for i in sorted(default)]

        self.response['status'] = True
        self.response['faturas'] = default

        return self.response

    def get_investments(self):
        investments = finance.models.Investment.objects.values('pk', 'name', 'dat_investment', 'amount_invested', 'price_investiment',
                                                               'qtd_titles', 'profit_contracted', 'description') \
            .annotate(id=F('pk'),
                      type=F('type__name'))

        response = {
            'status': True,
            'descricao': None,
            'investments': list(investments)
        }

        return response

    def get_extrato_investimentos(self):
        invest = finance.models.ExtratoAplicacao.objects.values('id', 'vlr_investido', 'vlr_bruto', 'vlr_liquido', 'referencia') \
            .filter(referencia=self.reference).annotate(nm_investimento=F('aplicacao__nm_descritivo')).order_by('aplicacao__nm_descritivo')

        self.response['status'] = True
        self.response['investimentos'] = list(invest)

        return self.response

    def import_csv_fatura(self, path=None, skiprows=0):
        itens = pd.DataFrame([])

        base_name = os.path.basename(path)
        name = os.path.splitext(base_name)
        self.reference = name[0].split('-')[1] + name[0].split('-')[2]

        for df in pd.read_csv(path, iterator=True, chunksize=10000, skiprows=skiprows):
            itens = itens.append(pd.DataFrame(df))

        lista_itens_retorno = []
        lista_itens = []
        for index, row in itens.iterrows():
            item = finance.models.FaturaImported()
            item.reference = self.reference
            item.data = datetime.strptime(row['date'], '%Y-%m-%d').date()
            item.amount = row['amount']
            item.amount_currency = row['amount']
            item.moeda_codigo = 'real'
            item.is_validado = False
            item.cat_referencia = row['category']
            item.description = row['title']
            item.cartao_credito_id = 'nubank'
            lista_itens_retorno.append(finance.serializers.FaturaSerializer(item).data)
            lista_itens.append(item)

        finance.models.CreditCardBill.objects.bulk_create(lista_itens)

        return lista_itens_retorno

    def get_fixed_expenses(self, expense_type):
        filters = {
            'reference': self.reference
        }

        excluders = {}

        fixed_expenses = finance.models.CategoryGroup.objects.values_list('category', flat=True).filter(group='fixed_expenses')
        if expense_type == 'fixed':
            filters['category__in'] = list(fixed_expenses)
        else:
            excluders['category__in'] = list(fixed_expenses)

        statement = finance.models.BankStatement.objects.values('category__description').annotate(total=Sum('amount')).filter(**filters).exclude(**excluders)
        bill = finance.models.CreditCardBill.objects.values('category__description').annotate(total=Sum('amount')).filter(**filters).exclude(**excluders)

        expenses = statement.union(bill)

        grouped_values = defaultdict(float)
        for info in list(expenses):
            grouped_values[info['category__description']] += float(info['total'])

        grouped_values = [{'category': year, 'total_amount': grouped_values[year]} for year in sorted(grouped_values, reverse=True)]
        response = {
            'status': True,
            'expenses': list(grouped_values)
        }

        return response

    def variable_expenses(self):
        filters = {
            'reference': self.reference
        }
        fixed_expenses = finance.models.CategoryGroup.objects.values_list('category', flat=True).filter(group='fixed_expenses')
        filters['category__in'] = list(fixed_expenses)

        statement = finance.models.BankStatement.objects.values('category__description').annotate(total=Sum('amount')).filter(**filters)
        bill = finance.models.CreditCardBill.objects.values('category__description').annotate(total=Sum('amount')).filter(**filters)

    def import_csv_investimento(self, path=None, skiprows=0):
        itens = pd.DataFrame([])

        df = pd.read_excel(path)

        print(df)

        for row in df.head().itertuples():
            print(row)

    def get_payment_date(self, dat_purchase, credit_card_id):
        card = finance.models.CreditCard.objects.filter(pk=credit_card_id, status=True).first()

        if not card or not dat_purchase:
            response = {
                'status': False,
                'description': _('Cartão de crédito não válido ou data de compra inválida')
            }
            return response

        day_close = card.dat_threshold
        day_payment = card.dat_payment

        dat_purchase = util.datetime.data_to_datetime(dat_purchase, formato='%d/%m/%Y')
        day_purchase = dat_purchase.day
        month_purchase = dat_purchase.month
        year_purchase = dat_purchase.year

        # TODO: there is a problem when threshold day is in previous month, then the simple rule of >= does not apply
        dat_payment = datetime(day=day_payment, month=month_purchase, year=year_purchase)
        if day_purchase >= day_close:
            dat_payment = dat_payment + relativedelta(months=1)

        response = {
            'status': True,
            'dat_payment': dat_payment.date()
        }
        print(dat_payment.date())
        return response

    def _set_referencia(self):
        dat_compra_date = util.datetime.data_to_datetime(self.dat_compra, formato='%d/%m/%Y')
        referencia_ano = dat_compra_date.year
        referencia_mes = dat_compra_date.month
        self.reference = referencia_ano * 100 + referencia_mes
