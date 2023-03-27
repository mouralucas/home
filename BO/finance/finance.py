from collections import defaultdict
from datetime import datetime

import camelot
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, F, Case, When, CharField, Value
from django.utils.translation import gettext_lazy as _
from tabula import read_pdf

import finance.models
import finance.serializers
import util.datetime


class Finance:

    def __init__(self, mes=None, ano=None, statement_id=None, bill_id=None, period=None, account_id=None, credit_card_id=None, amount=None,
                 amount_currency=None, price_currency_dollar=None, vlr_moeda=None, amount_tax=None, installment=None, tot_installment=None, dat_compra=None, dat_pagamento=None,
                 description=None, category_id=None, currency_id=None, price_dollar=None, cash_flow_id=None, owner=None):
        self.mes = mes
        self.ano = ano

        self.statement_id = statement_id
        self.bill_id = bill_id
        self.period = period
        self.amount = amount
        self.amount_currency = amount_currency
        self.price_currency_dollar = price_currency_dollar
        self.vlr_moeda = vlr_moeda
        self.amount_tax = amount_tax
        self.instalment = installment
        self.tot_installment = tot_installment
        self.dat_compra = dat_compra
        self.dat_pagamento = dat_pagamento
        self.description = description
        self.categoria_id = category_id
        self.account_id = account_id
        self.credit_card_id = credit_card_id
        self.currency_id = currency_id
        self.cash_flow_id = cash_flow_id
        self.owner = owner

        self.response = {}  # Deprecated

    def get_accounts(self):
        """
        :Name: get_bank_accounts
        :Description: get the list of accounts
        :Created by: Lucas Penha de Moura - 02/10/2022
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        None

        Return: the list of saved accounts
        """
        bank_accounts = finance.models.Account.objects\
            .values('id', 'nickname', 'branch_formatted', 'account_number_formatted', 'dat_open', 'dat_close').filter(owner=self.owner).active()

        response = {
            'status': True,
            'description': None,
            'quantity': len(bank_accounts),
            'accounts': list(bank_accounts),
        }

        return response

    def get_credit_cards(self):
        """
        :Name: get_credit_cards
        :Description: get the list of credit cards
        :Created by: Lucas Penha de Moura - 02/10/2022
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        None

        Return: the list of saved credit cards
        """
        # TODO: mudar para receber parâmetro de status
        credit_cards = finance.models.CreditCard.objects.values('id', 'name', 'description', 'dat_closing', 'dat_due').active() \
            .annotate(nm_status=Case(When(status=True, then=Value('Ativo')),
                                     default=Value('Cancelado'),
                                     output_field=CharField())).order_by('-status', 'id')

        response = {
            'status': True,
            'description': None,
            'quantity': len(credit_cards),
            'credit_cards': list(credit_cards),
        }

        return response

    def set_statement(self, request=None):
        if not self.dat_compra or not self.amount or not self.categoria_id or not self.account_id:
            response = {
                'status': False,
                'description': _('Todos os parâmetros são obrigatórios')
            }
            return response

        if self.statement_id:
            statement = finance.models.BankStatement.objects.filter(pk=self.statement_id).first()
        else:
            statement = finance.models.BankStatement()

        # Não modificado nomes
        self.__set_reference()

        if self.cash_flow_id == 'INCOMING':
            multiplier = 1
        else:
            multiplier = -1

        statement.period = self.period
        statement.currency_id = self.currency_id
        statement.amount = float(self.amount) * multiplier
        statement.amount_absolute = float(self.amount)
        statement.dat_purchase = self.dat_compra
        statement.description = self.description
        statement.category_id = self.categoria_id
        statement.account_id = self.account_id
        statement.is_validated = True
        statement.cash_flow = self.cash_flow_id
        statement.save(request_=request)

        response = self.get_statement()

        return response

    def get_statement(self):
        filters = {
            'account__owner_id': self.owner
        }

        if self.account_id:
            filters['account_id'] = self.account_id

        statement = finance.models.BankStatement.objects.values('id', 'period', 'dat_purchase', 'description') \
            .filter(**filters).active().annotate(statement_id=F('id'),
                                                 amount=F('amount'),
                                                 nm_account=F('account__nickname'),
                                                 account_id=F('account_id'),
                                                 nm_category=F('category__description'),
                                                 category_id=F('category_id'),
                                                 datCreated=F('dat_created'),
                                                 datLastEdited=F('dat_last_edited')
                                                 ) \
            .order_by('-dat_purchase')

        response = {
            'status': True,
            'statement': list(statement)
        }
        return response

    def set_bill(self, request=None):
        if not self.dat_compra or not self.amount or not self.categoria_id or not self.credit_card_id:
            response = {
                'status': False,
                'description': _('Todos os parâmetros são obrigatórios')
            }
            return response

        if self.bill_id:
            bill = finance.models.CreditCardBill.objects.filter(pk=self.bill_id).first()
        else:
            bill = finance.models.CreditCardBill()

        # Não modificado
        dat_pagamento_date = util.datetime.date_to_datetime(self.dat_pagamento, output_format='%Y-%m-%d')
        referencia_ano = dat_pagamento_date.year
        referencia_mes = dat_pagamento_date.month
        self.period = referencia_ano * 100 + referencia_mes

        bill.credit_card_id = self.credit_card_id
        # Dates
        bill.period = self.period
        bill.dat_payment = dat_pagamento_date
        bill.dat_purchase = util.datetime.date_to_datetime(self.dat_compra, output_format='%Y-%m-%d')

        # Amounts
        bill.amount = float(self.amount) * -1
        bill.amount_absolute = float(self.amount)
        bill.amount_total = self.amount  # TODO: modificar para adicionar o valor total de compras parceladas
        bill.amount_currency = float(self.amount) * -1
        bill.price_currency_dollar = self.price_currency_dollar
        bill.price_dollar = 1

        bill.currency_id = "BRL"
        bill.category_id = self.categoria_id

        bill.installment = 1
        bill.tot_installment = self.tot_installment
        bill.description = self.description

        bill.is_validated = True

        bill.cash_flow = 'OUTGOING'

        bill.save(request_=request)

        response = self.get_bill()

        return response

    def get_bill(self, credit_card_bill_id=None):
        filters = {}
        if credit_card_bill_id:
            # bills = bills.filter(id=credit_card_bill_id).first()
            filters['id'] = credit_card_bill_id

        else:
            filters = {
                'period': self.period
            }

            if self.credit_card_id:
                filters['credit_card_id'] = self.credit_card_id

        bills = finance.models.CreditCardBill.objects \
            .values('id', 'period', 'dat_purchase', 'dat_payment',
                    'installment', 'tot_installment', 'description') \
            .filter(**filters) \
            .annotate(amount=F('amount'),
                      credit_card_id=F('credit_card_id'),
                      nm_credit_card=F('credit_card__name'),
                      category_id=F('category_id'),
                      nm_category=F('category__description'),
                      datCreated=F('dat_created'),
                      datLastEdited=F('dat_last_edited')
                      ).order_by('dat_purchase')

        response = {
            'status': True,
            'bill': list(bills) if not credit_card_bill_id else bills
        }

        return response

    def get_bill_statistic(self):
        bills = finance.models.CreditCardBill.objects.all()
        qtd_total = bills.count()
        qtd_reference = bills.filter(reference=self.period).count()

        response = {
            'status': True,
            'qtd_total': qtd_total,
            'qtd_reference': qtd_reference,
        }

        return response

    def get_bill_history(self, period_start=201801, period_end=202302, months=13):
        history = finance.models.CreditCardBill.objects.values('period') \
            .annotate(total_amount=Sum('amount'),
                      total_amount_absolute=Sum('amount_absolute')) \
            .filter(period__range=(period_start, period_end)).order_by('period')

        average = sum(item['total_amount_absolute'] for item in history) / len(history) if history else 0

        response = {
            'success': True,
            'average': average,
            'goal': 2300,
            'history': list(history),
        }

        return response

    def get_category_history(self, months=13):
        fixed_expenses = finance.models.CategoryGroup.objects.values_list('category', flat=True).filter(group='fixed_expenses')
        filters = {
            'reference__range': (202001, 202012),
            'category__in': list(fixed_expenses)
        }

        bills = finance.models.CreditCardBill.objects.values('period', 'category__description') \
            .filter(**filters).annotate(total=Sum('amount')).order_by('period')

        statements = finance.models.BankStatement.objects.values('period', 'category__description') \
            .filter(**filters).annotate(total=Sum('amount')).order_by('period')

        evolucao = statements.union(bills)

        default = defaultdict(float)

        for i in list(evolucao):
            default[str(i.get('reference', '')) + '.' + i.get('category__description', '')] += float(i.get('total', 0))

        default = [{'reference': i.split('.')[0], 'categoria': i.split('.')[1], 'total': default[i]} for i in sorted(default)]

        self.response['status'] = True
        self.response['faturas'] = default

        return self.response

    def set_investment(self):

        response = self.get_investment()
        return response

    def get_investment(self):
        investments = finance.models.Investment.objects.values('pk', 'name', 'dat_investment', 'amount_invested', 'price_investment',
                                                               'qtd_titles', 'profit_contracted', 'description') \
            .annotate(id=F('pk'),
                      type=F('type__name'))

        response = {
            'status': True,
            'description': None,
            'investments': list(investments)
        }

        return response

    def get_summary(self):
        cat_not_expense = finance.models.CategoryGroup.objects.values_list('category_id', flat=True).filter(group='not_expense')

        credit_card_bill = finance.models.CreditCardBill.objects.values_list('amount', flat=True).filter(period=self.period)
        bank_statement = finance.models.BankStatement.objects.filter(period=self.period)
        bank_statement_incoming = sum(list(bank_statement.values_list('amount', flat=True)
                                           .filter(cash_flow='INCOMING').exclude(category_id__in=list(cat_not_expense))))
        bank_statement_outgoing = sum(list(bank_statement.values_list('amount', flat=True)
                                           .filter(cash_flow='OUTGOING').exclude(category_id__in=list(cat_not_expense))))
        bank_statement_balance = bank_statement_incoming + bank_statement_outgoing

        response = {
            'success': True,
            'period': self.period,
            'balance': bank_statement_balance,
            'incoming': bank_statement_incoming,
            'outgoing': bank_statement_outgoing,
            'credit': sum(list(credit_card_bill)),
            'credit_qtd': len(credit_card_bill),
        }

        return response

    def get_investment_statement(self):
        invest = finance.models.InvestmentStatement.objects.values('id', 'investment__amount_invested', 'vlr_bruto', 'vlr_liquido', 'referencia') \
            .filter(reference=self.period).annotate(nm_investimento=F('aplicacao__nm_descritivo')).order_by('aplicacao__nm_descritivo')

        self.response['success'] = True
        self.response['investment_statement'] = list(invest)

        return self.response

    def get_expenses(self, expense_type):
        filters = {
            'period': self.period
        }

        excluders = {}

        fixed_expenses = finance.models.CategoryGroup.objects.values_list('category', flat=True).filter(group='fixed_expenses')
        if expense_type == 'fixed':
            filters['category__in'] = list(fixed_expenses)
        else:
            excluders['category__in'] = list(fixed_expenses)
            excluders['total__gt'] = 0.0
            filters['total__lt'] = 0

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

    def get_category_expense(self):
        # Categorias que não são despesas representam transações que não afetam a quantidade de dinheiro em conta
        # Normalmente são categorias de transferências e depósitos para contas do mesmo titular
        cat_not_expense = finance.models.CategoryGroup.objects.values_list('category_id', flat=True).filter(group='not_expense')
        statement = finance.models.BankStatement.objects \
            .values('category__parent__description') \
            .annotate(category=F('category__parent__description'),
                      total=Sum('amount_absolute')) \
            .filter(period=self.period, cash_flow='OUTGOING').exclude(category_id__in=list(cat_not_expense))
        credit_card = finance.models.CreditCardBill.objects \
            .values('category__parent__description') \
            .annotate(category=F('category__parent__description'),
                      total=Sum('amount_absolute')) \
            .filter(period=self.period, cash_flow='OUTGOING').exclude(category_id__in=list(cat_not_expense))

        expenses = statement.union(credit_card)

        grouped_values = defaultdict(float)
        for info in list(expenses):
            grouped_values[info['category']] += float(info['total'])

        grouped_values = [{'category': year, 'total': grouped_values[year]} for year in sorted(grouped_values, reverse=True)]

        response = {
            'success': True,
            'expenses': list(grouped_values)
        }

        return response

    def get_credit_debit_proportion(self):
        pass

    def get_currency(self, is_shown=True):
        filters = {}

        if is_shown:
            filters['is_shown'] = True

        currency = finance.models.Currency.objects.values('id', 'name', 'symbol').filter(**filters)

        response = {
            'success': True,
            'currency': list(currency)
        }

        return response

    def get_due_date(self, dat_purchase, credit_card_id):
        card = finance.models.CreditCard.objects.filter(pk=credit_card_id, status=True).first()

        if not card or not dat_purchase:
            response = {
                'status': False,
                'description': _('Cartão de crédito não válido ou data de compra inválida')
            }
            return response

        day_close = card.dat_closing
        day_payment = card.dat_due

        dat_purchase = util.datetime.date_to_datetime(dat_purchase, output_format='%d/%m/%Y')
        day_purchase = dat_purchase.day
        month_purchase = dat_purchase.month
        year_purchase = dat_purchase.year

        # TODO: there is a problem when closing day is in previous month, then the simple rule of >= does not apply
        dat_payment = datetime(day=day_payment, month=month_purchase, year=year_purchase)
        if day_purchase >= day_close:
            dat_payment = dat_payment + relativedelta(months=1)

        response = {
            'status': True,
            'dat_payment': dat_payment.date()
        }
        print(dat_payment.date())
        return response

    def import_picpay_statement(self, path):
        new_columns = {
            'Data/Hora': 'date',
            'Descrição das Movimentações': 'description',
            'Valor': 'amount',
        }

        tables = camelot.read_pdf(path, pages='1-end')
        df = pd.concat([table.df.rename(columns=table.df.iloc[0]).drop(table.df.index[0]) for table in tables])
        df = df.rename(columns=new_columns)

        # Remove unnecessary columns
        df = df[df.columns[df.columns.isin(list(new_columns.values()))]]

        # Clean data
        df['date'] = df['date'].apply(lambda x: x.replace('\r', ' ').replace('\n', ' '))
        df['datetime'] = df['date'].apply(lambda x: util.datetime.DateTime.str_to_datetime(x.split(' ')[0], '%d/%m/%Y'))
        df['amount'] = df['amount'].apply(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', ''))
        df['amount'] = df['amount'].apply(lambda x: float(x))
        df['period'] = df['date'].apply(lambda x: util.datetime.DateTime.get_period(x.split(' ')[0], is_date_str=True, input_format='%d/%m/%Y'))

        list_period = df.groupby("period")
        for i in list_period:
            aux = i[1]
            aux['cumulated'] = aux['amount'].cumsum()
            print(aux)

        # list_statement = []
        # for idx, i in df.iterrows():
        #     statement = finance.models.BankStatement()
        #     statement.period = i['period']
        #     statement.amount = i['amount']
        #     statement.dat_purchase = i['datetime']
        #     statement.description = i['description']
        #     statement.is_validated = False
        #     statement.origin = 'PDF_IMPORT'
        #     statement.account_id = 'picpay'
        #     list_statement.append(statement)

        # finance.models.BankStatement.objects.bulk_create(list_statement)
        # df['acumulado'] = df.groupby(['date']).cumsum()

        df.to_excel('teste.xlsx', index=False)
        print('')

    def import_picpay_bill(self, path, period):
        df = read_pdf(path, pages="all", stream=False, pandas_options={'header': None})
        df[0].columns = ["date", "description", "amount_dollar", "amount"]
        df = df[0]
        df['date'] = df['date'].fillna("")
        df['day'] = df['date'].apply(lambda x: x.split(' ')[0] if x != np.nan else None)
        df['month'] = period[4:]
        df['year'] = period[:4]
        df['date_form'] = df['day']
        print(df.dtypes)
        print('')

    def __set_reference(self):
        dat_purchase = util.datetime.date_to_datetime(self.dat_compra, output_format='%Y-%m-%d')
        year = dat_purchase.year
        month = dat_purchase.month
        self.period = year * 100 + month
