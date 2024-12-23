import datetime
from datetime import datetime

import numpy as np
import pandas as pd
import pdfplumber
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from tabula import read_pdf

import finance.models
import finance.requests
import util.datetime
from finance.responses.account import StatementGetResponse


class Finance:
    # TODO: this must have only abstract methods, remove all others
    def __init__(self, mes=None, ano=None, statement_id=None, period=None, account_id=None, credit_card_id=None, amount=None,
                 amount_currency=None, price_currency_dollar=None, amount_tax=None, installment=None, tot_installment=None, purchase_at=None, payment_at=None,
                 description=None, category_id=None, currency_id=None, cash_flow_id=None, owner=None, request=None):
        self.request = request
        self.mes = mes
        self.ano = ano
        self.period = period
        self.purchase_at = purchase_at
        self.owner = owner
        self.amount = amount

    def get_expenses(self, category_id=None):
        pass

    def get_category_transactions_aggregated(self):
        # Categorias que não são despesas representam transações que não afetam a quantidade de dinheiro em conta
        # Normalmente são categorias de transferências e depósitos para contas do mesmo titular
        cat_not_expense = finance.models.CategoryGroup.objects.values_list('category_id', flat=True).filter(group='not_expense')

        filters = {
            'period': self.period,
            'cash_flow': 'OUTGOING',
            'owner_id': self.owner
        }

        statement = finance.models.AccountStatement.objects \
            .values('id') \
            .annotate(categoryId=F('category__parent_id'),
                      category=F('category__parent__description'),
                      total=Sum('amount_absolute')) \
            .filter(**filters).exclude(category_id__in=list(cat_not_expense))

        credit_card = finance.models.CreditCardBill.objects \
            .values('id') \
            .annotate(categoryId=F('category__parent_id'),
                      category=F('category__parent__description'),
                      total=Sum('amount_absolute')) \
            .filter(**filters).exclude(category_id__in=list(cat_not_expense))

        expenses = statement.union(credit_card)

        merged_data = {}
        for item in expenses:
            category_id = item["categoryId"]
            total = item["total"]
            if category_id in merged_data:
                # If category_id already exists, add the 'total' value
                merged_data[category_id]["total"] += total
            else:
                # If category_id is new, add the entire dictionary
                merged_data[category_id] = item

        response = {
            'success': True,
            'transactions': list(merged_data.values())
        }

        return response

    def get_credit_debit_proportion(self):
        pass

    def get_due_date(self, dat_purchase, credit_card_id):
        # TODO: Find a definitive solution to this problem
        card = finance.models.CreditCard.objects.filter(pk=credit_card_id, status=True).first()

        if not card or not dat_purchase:
            response = {
                'status': False,
                'description': _('Cartão de crédito não válido ou data de compra inválida')
            }
            return response

        day_close = card.closing_at
        day_payment = card.due_at

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

        tables = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                print(table)
                if table:
                    tables.append(table)

        df = pd.DataFrame()
        if tables:
            df = pd.DataFrame(columns=tables[0][0])
            for table in tables:
                df_novas_linhas = pd.DataFrame(table[1:], columns=df.columns)
                df = df.append(df_novas_linhas, ignore_index=True)

        # df = pd.concat([table.df.rename(columns=table.df.iloc[0]).drop(table.df.index[0]) for table in tables])
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
        # for idx, i in newdf.iterrows():
        #     statement = finance.models.AccountStatement()
        #     statement.period = i['period']
        #     statement.amount = i['amount']
        #     statement.amount_absolute = i['amount']
        #     statement.dat_purchase = i['datetime']
        #     statement.description = i['description']
        #     statement.is_validated = False
        #     statement.origin = 'PDF_IMPORT'
        #     statement.account_id = '32e542e7-bf2b-4408-b724-798591f11e09'
        #     statement.currency_id = 'BRL'
        #     statement.owner_id = 'adf52a1e-7a19-11ed-a1eb-0242ac120002'
        #     list_statement.append(statement)
        #
        # finance.models.AccountStatement.objects.bulk_create(list_statement)
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

    def import_pagbank_excel_statement(self, path, period):
        statement = pd.read_excel(path, sheet_name='Sheet0')

        print('')

    # Manter no service Finance, pois é função geral de finance, todas as específicas serão migrados (account, investment, credit card, etc.)
    def get_bank(self):
        bank = finance.models.Bank.objects.values('id', 'name', 'code').active()

        response = {
            'success': True,
            'bank': list(bank)
        }

        return response

    def get_summary(self):
        # TODO: update with new balance model
        cat_not_expense = finance.models.CategoryGroup.objects.values_list('category_id', flat=True).filter(group='not_expense')

        credit_card_bill = finance.models.CreditCardBill.objects.values_list('amount', flat=True).filter(period=self.period, owner_id=self.owner)
        bank_statement = finance.models.AccountStatement.objects.filter(period=self.period, owner_id=self.owner)

        bank_statement_incoming = sum(list(bank_statement.values_list('amount', flat=True).filter(cash_flow='INCOMING').exclude(category_id__in=list(cat_not_expense))))
        bank_statement_outgoing = sum(list(bank_statement.values_list('amount', flat=True).filter(cash_flow='OUTGOING').exclude(category_id__in=list(cat_not_expense))))
        bank_statement_balance = bank_statement_incoming + bank_statement_outgoing

        if self.period == util.datetime.current_period():
            reference_date = datetime.today()
        else:
            # Create function in datetime to date last day from period
            reference_date = '2023-10-13'

        summary = {
            'period': self.period,
            'referenceDate': reference_date,
            'periodIncoming': bank_statement_incoming,
            'periodOutgoing': bank_statement_outgoing,
            'periodBalance': bank_statement_balance,

            'periodCreditCardBill': sum(list(credit_card_bill)) * -1,
            'periodCreditCardPurchaseQuantity': len(credit_card_bill),
        }

        response = {
            'success': True,
            'summary': summary
        }

        return response

    def _set_period(self):
        year = self.purchase_at.year
        month = self.purchase_at.month
        self.period = year * 100 + month

    def _clean_account_info(self, value):
        if value is not None:
            number, digit = value.split('-')

            return {
                'number': number,
                'digit': digit
            }

        return value
