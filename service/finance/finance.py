import datetime
from collections import defaultdict
from datetime import datetime

import camelot
import numpy as np
import pandas as pd
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _
from tabula import read_pdf

import finance.models
import finance.serializers
import util.datetime


class Finance:

    def __init__(self, mes=None, ano=None, statement_id=None, bill_id=None, reference=None, account_id=None, credit_card_id=None, amount=None,
                 amount_currency=None, price_currency_dollar=None, vlr_moeda=None, amount_tax=None, installment=None, tot_installment=None, dat_compra=None, dat_pagamento=None,
                 description=None, category_id=None, currency_id=None, price_dollar=None, cash_flow_id=None, owner=None):
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
        self.instalment = installment
        self.tot_installment = tot_installment
        self.purchased_at = dat_compra
        self.dat_pagamento = dat_pagamento
        self.description = description
        self.categoria_id = category_id
        self.account_id = account_id
        self.credit_card_id = credit_card_id
        self.currency_id = currency_id
        self.cash_flow_id = cash_flow_id
        self.owner = owner

        self.response = {}  # Deprecated

    def set_statement(self, request=None):
        if not self.purchased_at or not self.amount or not self.categoria_id or not self.account_id:
            response = {
                'status': False,
                'description': _('Todos os parâmetros são obrigatórios')
            }
            return response

        if self.statement_id:
            statement = finance.models.BankStatement.objects.filter(pk=self.statement_id).first()
        else:
            statement = finance.models.BankStatement()

        self.__set_reference()

        # TODO: Essa lógica de entrada e saída está muito ruim
        if self.cash_flow_id == 'INCOMING':
            multiplier = 1
        else:
            # If amount already lower than zero no need to change again
            multiplier = -1 if float(self.amount) > 0 else 1

        statement.period = self.reference
        statement.currency_id = self.currency_id
        statement.amount = float(self.amount) * multiplier
        statement.amount_absolute = float(self.amount)
        statement.dat_purchase = self.purchased_at
        statement.description = self.description
        statement.category_id = self.categoria_id
        statement.account_id = self.account_id
        statement.is_validated = True
        statement.cash_flow = self.cash_flow_id
        statement.owner_id = self.owner
        statement.save(request_=request)

        response = self.get_statement()

        return response

    def get_statement(self):
        filters = {
            'owner_id': self.owner
        }

        if self.account_id:
            filters['account_id'] = self.account_id

        statement = finance.models.BankStatement.objects.values('period', 'description') \
            .filter(**filters).active().annotate(statementId=F('id'),
                                                 amount=F('amount'),
                                                 accountName=F('account__nickname'),
                                                 accountId=F('account_id'),
                                                 categoryName=F('category__description'),
                                                 categoryId=F('category_id'),
                                                 purchasedAt=F('dat_purchase'),
                                                 cashFlowId=F('cash_flow'),
                                                 currencyId=F('currency_id'),
                                                 currencySymbol=F('currency__symbol'),
                                                 createdAt=F('dat_created'),
                                                 lastEditedAt=F('dat_last_edited'),
                                                 ) \
            .order_by('-dat_purchase', '-dat_created')

        response = {
            'status': True,
            'statement': list(statement)
        }
        return response

    def get_bill_statistic(self):
        bills = finance.models.CreditCardBill.objects.filter(owner_id=self.owner)
        qtd_total = bills.count()
        qtd_reference = bills.filter(reference=self.reference).count()

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
            .filter(period__range=(period_start, period_end), owner_id=self.owner).order_by('period')

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
            'category__in': list(fixed_expenses),
            'owner_id': self.owner
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

    def get_expenses(self, expense_type):
        filters = {
            'period': self.reference,
            'owner_id': self.owner
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

        filters = {
            'period': self.reference,
            'cash_flow': 'OUTGOING',
            'owner_id': self.owner
        }

        statement = finance.models.BankStatement.objects \
            .values('category__parent__description') \
            .annotate(category=F('category__parent__description'),
                      total=Sum('amount_absolute')) \
            .filter(**filters).exclude(category_id__in=list(cat_not_expense))

        credit_card = finance.models.CreditCardBill.objects \
            .values('category__parent__description') \
            .annotate(category=F('category__parent__description'),
                      total=Sum('amount_absolute')) \
            .filter(**filters).exclude(category_id__in=list(cat_not_expense))

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

        dat_purchase = datetime.date(year=2023, month=4, day=27)

        if day_close > day_payment and dat_purchase.day < day_close:
            # add validação de mes de janeiro considerar ano anterior
            # add validação de mes de dezembro considerar próximo ano
            data_fechamento = datetime.date(dat_purchase.year, dat_purchase.month - 1, day_close)
            data_pagamento = datetime.date(dat_purchase.year, dat_purchase.month + 1, day_payment)

            print('Fechamento em {fec}, pagamento em {pag}'.format(fec=data_fechamento, pag=data_pagamento))
        else:
            print('Else')

        response = {}
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

        newdf = df[df['description'].str.contains("Rendimento")]

        list_period = df.groupby("period")
        for i in list_period:
            aux = i[1]
            aux['cumulated'] = aux['amount'].cumsum()
            print(aux)

        list_statement = []
        for idx, i in newdf.iterrows():
            statement = finance.models.BankStatement()
            statement.period = i['period']
            statement.amount = i['amount']
            statement.amount_absolute = i['amount']
            statement.dat_purchase = i['datetime']
            statement.description = i['description']
            statement.is_validated = False
            statement.origin = 'PDF_IMPORT'
            statement.account_id = '32e542e7-bf2b-4408-b724-798591f11e09'
            statement.currency_id = 'BRL'
            statement.owner_id = 'adf52a1e-7a19-11ed-a1eb-0242ac120002'
            list_statement.append(statement)

        finance.models.BankStatement.objects.bulk_create(list_statement)
        # df['acumulado'] = df.groupby(['date']).cumsum()

        newdf.to_excel('teste.xlsx', index=False)
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

    def import_pagbank_excel_statement(self, path, period):
        statement = pd.read_excel(path, sheet_name='Sheet0')

        print('')

    def __set_reference(self):
        # dat_purchase = util.datetime.date_to_datetime(self.dat_compra, output_format='%Y-%m-%d')
        year = self.purchased_at.year
        month = self.purchased_at.month
        self.reference = year * 100 + month

    # Manter no service Finance, pois é função geral de finance, todas as específicas serão migrados (account, investment, credit card, etc.)
    def get_bank(self):
        bank = finance.models.Bank.objects.values('id', 'name', 'code').active()

        response = {
            'success': True,
            'bank': list(bank)
        }

        return response

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

    def get_summary(self):
        cat_not_expense = finance.models.CategoryGroup.objects.values_list('category_id', flat=True).filter(group='not_expense')

        credit_card_bill = finance.models.CreditCardBill.objects.values_list('amount', flat=True).filter(period=self.reference, owner_id=self.owner)
        bank_statement = finance.models.BankStatement.objects.filter(period=self.reference, owner_id=self.owner)

        bank_statement_incoming = sum(list(bank_statement.values_list('amount', flat=True)
                                           .filter(cash_flow='INCOMING').exclude(category_id__in=list(cat_not_expense))))
        bank_statement_outgoing = sum(list(bank_statement.values_list('amount', flat=True)
                                           .filter(cash_flow='OUTGOING').exclude(category_id__in=list(cat_not_expense))))
        bank_statement_balance = bank_statement_incoming + bank_statement_outgoing

        response = {
            'success': True,
            'period': self.reference,
            'balance': bank_statement_balance,
            'incoming': bank_statement_incoming,
            'outgoing': bank_statement_outgoing,
            'credit': sum(list(credit_card_bill)),
            'credit_qtd': len(credit_card_bill),
        }

        return response