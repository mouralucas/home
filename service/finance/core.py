from django.db.models import F
from rest_framework import status

import finance.models
from service.finance.finance import Finance


class Core(Finance):
    def __init__(self, category_id=None, period=None):
        super().__init__(category_id=category_id, period=period)

    def get_category_transactions_list(self):
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
            .annotate(transactionId=F('id'),
                      date=F('purchased_at'),
                      amount=F('amount'),
                      description=F('description'),
                      categoryName=F('category__name')) \
            .filter(category__parent_id=self.category_id, period=self.period)
        bill = finance.models.CreditCardBill.objects.values('id') \
            .annotate(transactionId=F('id'),
                      date=F('purchase_at'),
                      amount=F('amount'),
                      description=F('description'),
                      categoryName=F('category__name')) \
            .filter(category__parent_id=self.category_id, period=self.period)

        expenses = statement.union(bill)

        response = {
            "success": True,
            "transactions": list(expenses)
        }

        return response

    def get_currency(self, is_shown=True):
        filters = {}

        if is_shown:
            filters['is_shown'] = True

        currency = finance.models.Currency.objects.values('name', 'symbol').annotate(currencyId=F('id')).filter(**filters)

        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(currency),
            'currencies': list(currency)
        }

        return response
