import pandas as pd
from django.db.models import Sum, F, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import status

import finance.models
from util import datetime
from finance.responses.account import AccountGetResponse, StatementPostResponse, StatementGetResponse
from service.finance.finance import Finance


class Account(Finance):
    def __init__(self, owner=None):
        super().__init__(owner=owner)

    def get_accounts(self, is_investment):
        """
        :Name: get_bank_accounts
        :Description: get the list of accounts
        :Created by: Lucas Penha de Moura - 02/10/2022
        :Edited by:

        Explicit params:
        :param is_investment: if True return only investment accounts

        Implicit params (passed in the class instance or set by other functions):
        :param self.owner: the owner of the account

        Return: the list of user (owner) accounts
        """
        accounts = (finance.models.Account.objects
                    .values('nickname')
                    .annotate(accountId=F('id'),
                              branch=F('branch_formatted'),
                              number=F('account_number_formatted'),
                              openAt=F('open_at'),
                              closeAt=F('close_at'))
                    .filter(owner=self.owner).active())

        response = AccountGetResponse({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(accounts),
            'accounts': list(accounts),
        }).data

        return response

    def get_statement(self, account_id=None, period=None):
        filters = {
            'owner_id': self.owner
        }

        if account_id:
            filters['account_id'] = account_id

        statement = finance.models.AccountStatement.objects.values('period', 'description') \
            .filter(**filters).active().annotate(statementEntryId=F('id'),
                                                 amount=F('amount'),
                                                 accountName=F('account__nickname'),
                                                 accountId=F('account_id'),
                                                 categoryName=F('category__description'),
                                                 categoryId=F('category_id'),
                                                 purchaseAt=F('purchase_at'),
                                                 cashFlowId=F('cash_flow'),
                                                 currencyId=F('currency_id'),
                                                 currencySymbol=F('currency__symbol'),
                                                 createdAt=F('created_at'),
                                                 lastEditedAt=F('edited_at'),
                                                 ) \
            .order_by('-purchase_at', '-created_at')

        response = StatementGetResponse({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(statement),
            'statementEntry': statement
        }).data

        return response

    def set_statement(self, data, request=None):
        if data.get('statementId'):
            statement = finance.models.AccountStatement.objects.filter(pk=data.get('statementId')).first()
        else:
            statement = finance.models.AccountStatement()

        self.purchase_at = data.get('purchaseAt')
        self._set_period()

        # TODO: Essa lógica de entrada e saída está muito ruim
        if data.get('cashFlowId') == 'INCOMING':
            multiplier = 1
        else:
            # If amount already lower than zero no need to change again
            multiplier = -1 if float(data.get('amount')) > 0 else 1

        statement.period = self.period
        statement.currency_id = data.get('currencyId')
        statement.amount = float(data.get('amount')) * multiplier
        statement.amount_absolute = data.get('amount')
        statement.purchase_at = data.get('purchaseAt')
        statement.description = data.get('description')
        statement.category_id = data.get('categoryId')
        statement.account_id = data.get('accountId')
        statement.is_validated = True
        statement.cash_flow = data.get('cashFlowId')
        statement.owner_id = self.owner
        statement.save(request_=request)

        # TODO: the statement entry may be upgraded
        response = StatementPostResponse({
            'success': True,
            'statusCode': status.HTTP_201_CREATED,
            'statementEntry': {
                'statementEntryId': statement.id,
                'amount': statement.amount,
                'accountName': statement.account.nickname,
                'accountId': statement.account_id,
                'categoryName': statement.category.name,
                'categoryId': statement.category_id,
                'purchaseAt': statement.purchase_at,
                'cashFlowId': statement.cash_flow,
                'currencyId': statement.currency_id,
                'currencySymbol': statement.currency.symbol,
                'createdAt': statement.created_at,
                'lastEditedAt': statement.edited_at,
                'description': statement.description
            }
        }).data

        return response

    def get_statement_beta(self):

        previous_balance = finance.models.AccountStatement.objects.filter(period__lt=self.period, owner=self.owner, status=True).aggregate(tot=Sum('amount'))
        statement = finance.models.AccountStatement.objects.values('amount', 'description').filter(period=self.period, owner=self.owner, status=True)

        return {
            'success': True,
            'previous': previous_balance['tot'],
            'statement': list(statement)
        }

    def set_balance(self, account_id=None, start_period=None):
        filters = {}

        if start_period:
            filters['period__gte'] = start_period

        account_registers = finance.models.AccountStatement.objects.values('period') \
            .filter(account_id=account_id, status=True).filter(**filters).order_by('period')

        incoming = pd.DataFrame(account_registers.exclude(category_id__in=['rendimento']).filter(cash_flow='INCOMING').annotate(incoming=Sum('amount')))
        outgoing = pd.DataFrame(account_registers.exclude(category_id__in=['rendimento']).filter(cash_flow='OUTGOING').annotate(outgoing=Sum('amount')))
        transactions = pd.DataFrame(account_registers.exclude(category_id__in=['rendimento']).annotate(transactions=Sum('amount')))
        transactions = pd.merge(transactions, incoming, on='period', how='outer')
        transactions = pd.merge(transactions, outgoing, on='period', how='outer')
        if transactions.empty:
            transactions = pd.DataFrame(columns=['period', 'transactions'])

        earnings = pd.DataFrame(account_registers.filter(category_id='rendimento').annotate(earnings=Sum('amount')))
        if earnings.empty:
            earnings = pd.DataFrame(columns=['period', 'earnings'])

        merged_df = pd.merge(transactions, earnings, on='period', how='outer')
        merged_df = merged_df.fillna(0)
        merged_df['transaction_balance'] = merged_df['transactions'] + merged_df['earnings']

        merged_df['balance'] = merged_df['transaction_balance'].cumsum()

        # Set min and max periods for each account
        account = finance.models.Account.objects.filter(pk=account_id).first()
        min_period = merged_df['period'].min()
        max_period = datetime.get_period_from_date(account.close_at) if account.close_at else datetime.current_period()
        all_periods = list(range(min_period, max_period + 1))
        missing_periods = [p for p in all_periods if p not in merged_df['period'].tolist() and 12 >= p % 100 > 1]

        # Create row with missing reference
        new_rows = []
        for missing_period in missing_periods:
            prev_period = merged_df[merged_df['period'] < missing_period]['period'].max()
            prev_balance = merged_df[merged_df['period'] == prev_period]['balance'].values[0]

            new_row = {
                'period': missing_period,
                'transactions': 0,
                'earnings': 0,
                'transaction_balance': 0,
                'balance': prev_balance
            }
            new_rows.append(pd.DataFrame([new_row]))

        # Add missing reference to existing DF
        merged_df = pd.concat([merged_df] + new_rows, ignore_index=True)
        merged_df = merged_df.sort_values(by='period')
        merged_df['balance'] = merged_df['transaction_balance'].cumsum()
        merged_df = merged_df.fillna(0)

        balance_list = []
        for idx, balance in merged_df.iterrows():
            aux = finance.models.AccountBalance(
                created_at=timezone.now(),
                account_id=account_id,
                period=balance['period'],
                previous_balance=merged_df.at[idx - 1, 'balance'] if idx > 0 else 0,
                incoming=balance['incoming'],
                outgoing=balance['outgoing'],
                transactions=balance['transactions'],
                earnings=balance['earnings'],
                transactions_balance=balance['transaction_balance'],
                balance=balance['balance']
            )
            balance_list.append(aux)
        finance.models.AccountBalance.objects.filter(account_id=account_id).filter(**filters).delete()
        balance = finance.models.AccountBalance.objects.bulk_create(balance_list)

        response = {
            'success': True,
            'periods_saved': len(balance)
        }

        return response

    def get_balance_tests(self):
        subquery = (
            finance.models.AccountStatement.objects
            .filter(owner_id=self.owner, account_id='f211dc0e-411e-4728-b7cd-ef3b91f4ddb5', status=True, period__lt=OuterRef('period'))
            .values('period')
            .annotate(
                previous_period_balance=Sum('amount')
            )
            .order_by()
            .values('previous_period_balance')[:1]
        )

        query = (
            finance.models.AccountStatement.objects
            .filter(owner_id=self.owner, account_id='f211dc0e-411e-4728-b7cd-ef3b91f4ddb5', status=True)
            .values('period')
            .annotate(
                current_period_balance=Sum('amount'),
                previous_period_balance=Coalesce(Subquery(subquery), 0),
                current_balance=F('current_period_balance') + Coalesce(Subquery(subquery), 0)
            )
            .order_by('period')
        )

        response = {
            'success': True,
            'balance': list(query)
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
