from django.db.models import Sum
from rest_framework.views import APIView

import finance.models


class Balance(APIView):
    def get(self, *args, **kwargs):
        teste = []
        for i in range(201801, 201813):
            balance = finance.models.BankStatement.objects.values('period', 'account_id')\
                .annotate(balance=Sum('amount')).filter(period=i, account_id='bb').exclude(category_id='saldo_anterior')

            teste += list(balance)

        print('')