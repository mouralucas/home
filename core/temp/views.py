import pandas
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

import finance.models
from django.utils import timezone


class Balance(APIView):
    def get(self, *args, **kwargs):
        balance_list = []
        start = 202201
        end = 202213
        # accounts = finance.models.BankStatement.objects.values_list('account_id', flat=True).filter(period__range=(start, end)).distinct()
        accounts = ['32e542e7-bf2b-4408-b724-798591f11e09']
        for j in accounts:
            for i in range(start, end):
                print('Searching {period} for {bank}'.format(period=i, bank=j))
                statement = finance.models.BankStatement.objects \
                    .filter(period__lte=i, account_id=j)

                # O valor só da certo no primeiro mês, não esta considerando o "saldo anterior" pq não soma o rendimento
                balance = statement \
                    .exclude(category_id__in=['saldo_anterior', 'rendimento']).aggregate(balance=Sum('amount'))

                earning = finance.models.BankStatement.objects.filter(period=i, account_id=j, category_id='rendimento').aggregate(earning=Sum('amount'))

                total = statement \
                    .exclude(category_id__in=['saldo_anterior']).aggregate(total=Sum('amount'))

                earnings = earning['earning'] if earning['earning'] else 0
                total_amount = total['total'] if total['total'] else 0
                balance_amount = total_amount - earnings

                aux = {
                    'account': j,
                    'period': i,
                    'balance': balance_amount,
                    'earning': earnings,
                    'total_amount': total_amount
                }
                balance_list.append(aux)

        my_user = 'adf52a1e-7a19-11ed-a1eb-0242ac120002'

        balance_list_model = []
        for i in balance_list:
            if i['balance'] is not None:
                aux = finance.models.BankAccountMonthlyBalance(
                    dat_created=timezone.now(),
                    account_id=i['account'],
                    amount=i['balance'],
                    period=i['period'],
                    earning=i['earning'],
                    total_amount=i['total_amount'],
                    created_by_id=my_user
                )
                balance_list_model.append(aux)

        finance.models.BankAccountMonthlyBalance.objects.bulk_create(balance_list_model)
        return Response(balance_list)


class Statement(APIView):
    def get(self, *args, **kwargs):
        accounts = finance.models.Account.objects.values_list('id', flat=True).filter(owner_id='adf52a1e-7a19-11ed-a1eb-0242ac120002')
        accounts = ['a7b2cb0c-c64e-4623-9673-72c6205ad2e1']

        statement_dict = {}
        total_anterior = 0
        for idx, account in enumerate(accounts):
            period_totals = pandas.DataFrame(finance.models.BankStatement.objects.values('period').annotate(tot=Sum('amount'))
                             .filter(account_id=account, status=True, period__lte=202312).order_by('period'))

            period_totals['statement'] = period_totals['tot'].cumsum()

            return Response(period_totals.to_json, status=200)

