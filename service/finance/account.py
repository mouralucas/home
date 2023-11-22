import pandas as pd
from django.db.models import Sum, F, Window, Subquery, OuterRef
from django.db.models.functions import Lag, Coalesce
from django.utils import timezone

import finance.models
import util.datetime
from service.finance.finance import Finance
from rest_framework import status


class Account(Finance):
    def __init__(self, owner=None, account_id=None, period=None):
        super().__init__(owner=owner, account_id=account_id, period=period)

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
        bank_accounts = (finance.models.Account.objects
                         .values('id', 'nickname')
                         .annotate(branchFormated=F('branch_formatted'),
                                   accountNumberFormatted=F('account_number_formatted'),
                                   openAt=F('open_at'),
                                   closeAt=F('close_at'))
                         .filter(owner=self.owner).active())

        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(bank_accounts),
            'accounts': list(bank_accounts),
        }

        return response

    def get_statement_beta(self):

        previous_balance = finance.models.AccountStatement.objects.filter(period__lt=self.period, owner=self.owner, status=True).aggregate(tot=Sum('amount'))
        statement = finance.models.AccountStatement.objects.values('amount', 'description').filter(period=self.period, owner=self.owner, status=True)

        return {
            'success': True,
            'previous': previous_balance['tot'],
            'statement': list(statement)
        }

    def set_balance(self, start_period=None):
        filters = {}

        if start_period:
            filters['period__gte'] = start_period

        account_registers = finance.models.AccountStatement.objects.values('period') \
            .filter(account_id=self.account_id, status=True).filter(**filters).order_by('period')

        incoming = pd.DataFrame(account_registers.exclude(category_id__in=['rendimento']).filter(cash_flow='INCOMING').annotate(incoming=Sum('amount')))
        outgoing = pd.DataFrame(account_registers.exclude(category_id__in=['rendimento']).filter(cash_flow='OUTGOING').annotate(outgoing=Sum('amount')))
        transactions = pd.DataFrame(account_registers.exclude(category_id__in=['rendimento']).annotate(transactions=Sum('amount')))
        transactions = pd.merge(transactions, incoming, on='reference', how='outer')
        transactions = pd.merge(transactions, outgoing, on='reference', how='outer')
        if transactions.empty:
            transactions = pd.DataFrame(columns=['period', 'transactions'])

        earnings = pd.DataFrame(account_registers.filter(category_id='rendimento').annotate(earnings=Sum('amount')))
        if earnings.empty:
            earnings = pd.DataFrame(columns=['reference', 'earnings'])

        merged_df = pd.merge(transactions, earnings, on='reference', how='outer')
        merged_df = merged_df.fillna(0)
        merged_df['transaction_balance'] = merged_df['transactions'] + merged_df['earnings']

        merged_df['balance'] = merged_df['transaction_balance'].cumsum()

        # Set min and max periods for each account
        account = finance.models.Account.objects.filter(pk=self.account_id).first()
        min_period = merged_df['reference'].min()
        max_period = util.datetime.DateTime().get_period(account.close_at) if account.close_at else util.datetime.DateTime().current_period()
        all_periods = list(range(min_period, max_period + 1))
        missing_periods = [p for p in all_periods if p not in merged_df['reference'].tolist() and 12 >= p % 100 > 1]

        # Create row with missing reference
        new_rows = []
        for missing_period in missing_periods:
            prev_period = merged_df[merged_df['reference'] < missing_period]['reference'].max()
            prev_balance = merged_df[merged_df['reference'] == prev_period]['balance'].values[0]

            new_row = {
                'reference': missing_period,
                'transactions': 0,
                'earnings': 0,
                'transaction_balance': 0,
                'balance': prev_balance
            }
            new_rows.append(pd.DataFrame([new_row]))

        # Add missing reference to existing DF
        merged_df = pd.concat([merged_df] + new_rows, ignore_index=True)
        merged_df = merged_df.sort_values(by='reference')
        merged_df['balance'] = merged_df['transaction_balance'].cumsum()
        merged_df = merged_df.fillna(0)

        balance_list = []
        for idx, balance in merged_df.iterrows():
            aux = finance.models.AccountBalance(
                created_at=timezone.now(),
                account_id=self.account_id,
                reference=balance['reference'],
                previous_balance=0,
                incoming=balance['incoming'],
                outgoing=balance['outgoing'],
                transactions=balance['transactions'],
                earnings=balance['earnings'],
                transactions_balance=balance['transaction_balance'],
                balance=balance['balance']
            )
            balance_list.append(aux)
        finance.models.AccountBalance.objects.filter(account_id=self.account_id).filter(**filters).delete()
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
