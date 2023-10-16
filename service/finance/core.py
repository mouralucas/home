from django.db.models import F

import finance.models
from service.finance.finance import Finance


class Core(Finance):
    def __init__(self, category_id=None, period=None):
        super().__init__(category_id=category_id, period=period)

    def get_expense(self):
        """
        :Name: get_expense
        :Description: get the list of expenses based on filters
        :Created by: Lucas Penha de Moura - 13/10/2023
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        self.category_id: Category id

        Return: the list of saved accounts
        """
        statement = finance.models.AccountStatement.objects.values('id') \
            .annotate(date=F('purchased_at'),
                      amount=F('amount'),
                      description=F('Description')) \
            .filter(category_id=self.category_id)
        bill = finance.models.CreditCardBill.objects.values('id') \
            .annotate(date=F('purchased_at'),
                      amount=F('amount'),
                      description=F('Description')) \
            .filter(category_id=self.category_id)

        expenses = statement.union(bill)

        response = {
            "success": True,
            "expanses": list(expenses)
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
