import datetime
from datetime import datetime

import numpy as np
import pandas as pd
import pdfplumber
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _
from tabula import read_pdf

import finance.models
import finance.serializers
import util.datetime


class Finance:
    # TODO: this must have only abstract methods, remove all others
    def __init__(self, mes=None, ano=None, statement_id=None, bill_id=None, period=None, account_id=None, credit_card_id=None, amount=None,
                 amount_currency=None, price_currency_dollar=None, amount_tax=None, installment=None, tot_installment=None, dat_compra=None, dat_pagamento=None,
                 description=None, category_id=None, currency_id=None, cash_flow_id=None, owner=None):
        self.mes = mes
        self.ano = ano

        self.statement_id = statement_id
        self.bill_id = bill_id
        self.period = period
        self.amount = amount
        self.amount_currency = amount_currency
        self.price_currency_dollar = price_currency_dollar
        self.amount_tax = amount_tax
        self.instalment = installment
        self.tot_installment = tot_installment
        self.purchased_at = dat_compra
        self.dat_pagamento = dat_pagamento
        self.description = description
        self.category_id = category_id
        self.account_id = account_id
        self.credit_card_id = credit_card_id
        self.currency_id = currency_id
        self.cash_flow_id = cash_flow_id
        self.owner = owner

    def set_statement(self, request=None):
        # TODO: adicionar uma lógica que verifica a data da transação e se não for período anterior adicionar um uma tabela a informação pra reprocessar
        #   todo o extrato a partir do mês da transação
        if not self.purchased_at or not self.amount or not self.category_id or not self.account_id:
            response = {
                'status': False,
                'description': _('Todos os parâmetros são obrigatórios')
            }
            return response

        if self.statement_id:
            statement = finance.models.AccountStatement.objects.filter(pk=self.statement_id).first()
        else:
            statement = finance.models.AccountStatement()

        self.__set_period()

        # TODO: Essa lógica de entrada e saída está muito ruim
        if self.cash_flow_id == 'INCOMING':
            multiplier = 1
        else:
            # If amount already lower than zero no need to change again
            multiplier = -1 if float(self.amount) > 0 else 1

        statement.period = self.period
        statement.currency_id = self.currency_id
        statement.amount = float(self.amount) * multiplier
        statement.amount_absolute = float(self.amount)
        statement.purchase_at = self.purchased_at
        statement.description = self.description
        statement.category_id = self.category_id
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

        statement = finance.models.AccountStatement.objects.values('period', 'description') \
            .filter(**filters).active().annotate(statementId=F('id'),
                                                 amount=F('amount'),
                                                 accountName=F('account__nickname'),
                                                 accountId=F('account_id'),
                                                 categoryName=F('category__description'),
                                                 categoryId=F('category_id'),
                                                 purchasedAt=F('purchase_at'),
                                                 cashFlowId=F('cash_flow'),
                                                 currencyId=F('currency_id'),
                                                 currencySymbol=F('currency__symbol'),
                                                 createdAt=F('created_at'),
                                                 lastEditedAt=F('edited_at'),
                                                 ) \
            .order_by('-purchase_at', '-created_at')

        response = {
            'status': True,
            'statement': list(statement)
        }
        return response

    def get_bill_statistic(self):
        bills = finance.models.CreditCardBill.objects.filter(owner_id=self.owner)
        qtd_total = bills.count()
        qtd_period = bills.filter(period=self.period).count()

        response = {
            'status': True,
            'qtd_total': qtd_total,
            'qtd_period': qtd_period,
        }

        return response

    # def get_category_history(self, months=13):
    #     fixed_expenses = finance.models.CategoryGroup.objects.values_list('category', flat=True).filter(group='fixed_expenses')
    #     filters = {
    #         'period__range': (202001, 202012),
    #         'category__in': list(fixed_expenses),
    #         'owner_id': self.owner
    #     }
    #
    #     bills = finance.models.CreditCardBill.objects.values('period', 'category__description') \
    #         .filter(**filters).annotate(total=Sum('amount')).order_by('period')
    #
    #     statements = finance.models.AccountStatement.objects.values('period', 'category__description') \
    #         .filter(**filters).annotate(total=Sum('amount')).order_by('period')
    #
    #     evolucao = statements.union(bills)
    #
    #     default = defaultdict(float)
    #
    #     for i in list(evolucao):
    #         default[str(i.get('period', '')) + '.' + i.get('category__description', '')] += float(i.get('total', 0))
    #
    #     default = [{'period': i.split('.')[0], 'categoria': i.split('.')[1], 'total': default[i]} for i in sorted(default)]
    #
    #     self.response['status'] = True
    #     self.response['faturas'] = default
    #
    #     return self.response

    def get_expenses(self):
        self.category_id = None

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

        summary = {
            'period': self.period,
            'referenceDate': '2023-10-13',
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

    def __set_period(self):
        # dat_purchase = util.datetime.date_to_datetime(self.dat_compra, output_format='%Y-%m-%d')
        year = self.purchased_at.year
        month = self.purchased_at.month
        self.period = year * 100 + month
