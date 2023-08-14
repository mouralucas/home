import pandas
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

import finance.models
from django.utils import timezone


class Balance(APIView):
    def get(self, *args, **kwargs):
        pass
        # balance_list = []
        # start = 202201
        # end = 202213
        # # accounts = finance.models.BankStatement.objects.values_list('account_id', flat=True).filter(period__range=(start, end)).distinct()
        # accounts = ['32e542e7-bf2b-4408-b724-798591f11e09']
        # for j in accounts:
        #     for i in range(start, end):
        #         print('Searching {period} for {bank}'.format(period=i, bank=j))
        #         statement = finance.models.AccountStatement.objects \
        #             .filter(period__lte=i, account_id=j)
        #
        #         # O valor só da certo no primeiro mês, não esta considerando o "saldo anterior" pq não soma o rendimento
        #         balance = statement \
        #             .exclude(category_id__in=['saldo_anterior', 'rendimento']).aggregate(balance=Sum('amount'))
        #
        #         earning = finance.models.AccountStatement.objects.filter(period=i, account_id=j, category_id='rendimento').aggregate(earning=Sum('amount'))
        #
        #         total = statement \
        #             .exclude(category_id__in=['saldo_anterior']).aggregate(total=Sum('amount'))
        #
        #         earnings = earning['earning'] if earning['earning'] else 0
        #         total_amount = total['total'] if total['total'] else 0
        #         balance_amount = total_amount - earnings
        #
        #         aux = {
        #             'account': j,
        #             'period': i,
        #             'balance': balance_amount,
        #             'earning': earnings,
        #             'total_amount': total_amount
        #         }
        #         balance_list.append(aux)
        #
        # my_user = 'adf52a1e-7a19-11ed-a1eb-0242ac120002'
        #
        # balance_list_model = []
        # for i in balance_list:
        #     if i['balance'] is not None:
        #         aux = finance.models.BankAccountMonthlyBalance(
        #             dat_created=timezone.now(),
        #             account_id=i['account'],
        #             amount=i['balance'],
        #             period=i['period'],
        #             earning=i['earning'],
        #             total_amount=i['total_amount'],
        #             created_by_id=my_user
        #         )
        #         balance_list_model.append(aux)
        #
        # finance.models.BankAccountMonthlyBalance.objects.bulk_create(balance_list_model)
        # return Response(balance_list)


class Statement(APIView):
    def get(self, *args, **kwargs):
        accounts = finance.models.Account.objects.values_list('id', flat=True).filter(owner_id='adf52a1e-7a19-11ed-a1eb-0242ac120002')
        accounts = ['32e542e7-bf2b-4408-b724-798591f11e09']

        statement_dict = {}
        total_anterior = 0
        for idx, account in enumerate(accounts):
            account_registers = finance.models.AccountStatement.objects.values('period') \
                .filter(account_id=account, status=True).order_by('period')

            transactions = pandas.DataFrame(account_registers.exclude(category_id__in=['rendimento']).annotate(transaction=Sum('amount')))
            earnings = pandas.DataFrame(account_registers.filter(category_id='rendimento').annotate(earning=Sum('amount')))

            merged_df = pandas.merge(transactions, earnings, on='period', how='outer')
            merged_df = merged_df.sort_values(by='period')
            merged_df = merged_df.fillna(0)
            merged_df['transaction_balance'] = merged_df['transaction'] + merged_df['earning']

            merged_df['account_balance'] = merged_df['transaction_balance'].cumsum()

            return Response(period_totals.to_dict(), status=200)
