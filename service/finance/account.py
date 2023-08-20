import pandas as pd
from django.db.models import Sum
from django.utils import timezone

import finance.models
import service.finance.finance
import util.datetime


class Account(service.finance.finance.Finance):
    def __init__(self, owner=None, account_id=None):
        super().__init__(owner=owner)
        self.account_id = account_id

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
        bank_accounts = finance.models.Account.objects \
            .values('id', 'nickname', 'branch_formatted', 'account_number_formatted', 'dat_open', 'dat_close').filter(owner=self.owner).active()

        response = {
            'status': True,
            'description': None,
            'quantity': len(bank_accounts),
            'accounts': list(bank_accounts),
        }

        return response

    def set_balance(self, start_period=None):
        filters = {}

        if start_period:
            filters['period__get'] = start_period

        account_registers = finance.models.AccountStatement.objects.values('period') \
            .filter(account_id=self.account_id, status=True).filter(**filters).order_by('period')

        transactions = pd.DataFrame(account_registers.exclude(category_id__in=['rendimento']).annotate(transactions=Sum('amount')))
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
        account = finance.models.Account.objects.filter(pk=self.account_id).first()
        min_period = merged_df['period'].min()
        max_period = util.datetime.DateTime().get_period(account.dat_close) if account.dat_close else util.datetime.DateTime().current_period()
        all_periods = list(range(min_period, max_period + 1))
        missing_periods = [p for p in all_periods if p not in merged_df['period'].tolist() and 12 >= p % 100 > 1]

        # Create row with missing periods
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

        # Concatenar os DataFrames do período ausente ao DataFrame original
        merged_df = pd.concat([merged_df] + new_rows, ignore_index=True)
        merged_df = merged_df.sort_values(by='period')
        merged_df['balance'] = merged_df['transaction_balance'].cumsum()

        balance_list = []
        for idx, balance in merged_df.iterrows():
            aux = finance.models.AccountBalance(
                dat_created=timezone.now(),
                account_id=self.account_id,
                period=balance['period'],
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

