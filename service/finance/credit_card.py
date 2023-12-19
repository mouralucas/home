from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _
from rest_framework import status

import finance.models
import util.datetime
from service.finance.finance import Finance


class CreditCard(Finance):
    def __init__(self, owner=None):

        super().__init__(owner=owner)

    def get_credit_card(self):
        """
        :Name: get_credit_cards
        :Description: get the list of credit cards
        :Created by: Lucas Penha de Moura - 02/10/2022
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        None

        Return: the list of saved credit cards
        """
        # TODO: mudar para receber parâmetro de status
        credit_cards = (finance.models.CreditCard.objects.values('name', 'description')
                        .annotate(creditCardId=F('id'),
                                  closingAt=F('closing_at'),
                                  dueAt=F('due_at'))
                        .active().order_by('-status', 'id'))

        response = {
            'success': True,
            'message': None,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(credit_cards),
            'creditCards': list(credit_cards),
        }

        return response

    def get_credit_card_bill(self, period=None, credit_card_id=None, credit_card_bill_id=None):
        filters = {
            'owner_id': self.owner
        }
        if credit_card_bill_id:
            filters['id'] = credit_card_bill_id

        else:
            # filters['period'] = period
            pass

            if credit_card_id:
                filters['credit_card_id'] = credit_card_id

        bills = finance.models.CreditCardBill.objects \
            .values('id', 'period',
                    'installment', 'description') \
            .filter(**filters) \
            .annotate(amount=F('amount'),
                      purchaseAt=F('purchase_at'),
                      paymentAt=F('payment_at'),
                      creditCardId=F('credit_card_id'),
                      creditCardName=F('credit_card__name'),
                      categoryId=F('category_id'),
                      categoryName=F('category__description'),
                      createdAt=F('created_at'),
                      lastEditedAt=F('edited_at'),
                      totalInstallment=F('tot_installment')
                      ).order_by('-purchase_at', '-created_at')

        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'quantity': len(bills) if not credit_card_bill_id else 1,
            'bill': list(bills) if not credit_card_bill_id else bills
        }

        return response

    def set_bill(self, data, request=None):
        if data.get('creditCardBillId'):
            bill = finance.models.CreditCardBill.objects.filter(pk=data.get('creditCardBillId')).first()
        else:
            bill = finance.models.CreditCardBill()

        self.purchase_at = data.get('purchaseAt')
        year = data.get('paymentAt').year
        month = data.get('paymentAt').year
        self.period = year * 100 + month

        # Basic
        bill.credit_card_id = data.get('creditCardId')

        # Dates
        bill.period = self.period
        bill.payment_at = data.get('paymentAt')
        bill.purchase_at = data.get('purchaseAt')

        # Amounts
        bill.amount = data.get('amount') * -1
        bill.amount_absolute = data.get('amount')
        bill.amount_total = data.get('amount')  # TODO: modificar para adicionar o valor total de compras parceladas
        bill.amount_reference = data.get('amount') * -1  # vai vir da tela
        bill.dollar_currency_quote = data.get('dollarCurrencyQuote')
        bill.dollar_quote = 1  # vai vir da tela

        bill.currency_id = data.get('currencyId')
        bill.category_id = data.get('categoryId')

        bill.installment = data.get('installment')
        bill.tot_installment = data.get('installmentTotal')
        bill.description = data.get('description')

        bill.is_validated = True
        bill.cash_flow = data.get('cashFlowId')
        bill.currency_reference_id = 'BRL'
        bill.owner_id = self.owner

        bill.save(request_=request)

        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK
        }

        return response

    def get_bill_history(self, history_type, start_at, end_at):
        filters = {
            'owner_id': self.owner,
            'period__range': (start_at, end_at)
        }

        history = finance.models.CreditCardBill.objects.filter(**filters).order_by('period')

        if history_type == 'aggregated':
            return self.__get_bill_history_aggregated(history=history)

        if history_type == 'byCard':
            return self.__get_bill_history_card(history=history)

    def __get_bill_history_card(self, history):
        """
        :Name: get_bill_history_aggregated
        :Created by: Lucas Penha de Moura - 20/10/2023
        :Edited by:

        Explicit params:
        :param history: The complete queryset of history

        Implicit params (passed in the class instance or set by other functions):
        self.owner: the owner of the cards (logged user)

        Get the credit card expenses from all users cards by period/card
        """
        cards = history.values('credit_card_id').annotate(creditCardName=F('credit_card__name'), creditCardId=F('credit_card_id')).distinct('credit_card_id').order_by('credit_card_id')
        history = history.values('period', 'credit_card_id') \
            .annotate(creditCardName=F('credit_card__name'),
                      balance=Sum('amount') * -1)
        transformed_data = {}

        for item in history:
            period = item["period"]
            card_id = item["credit_card_id"]
            balance = item["balance"]

            if period not in transformed_data:
                transformed_data[period] = {
                    "id": period,
                    "period": period,
                    "total": 0,
                }

            transformed_data[period][card_id] = balance
            transformed_data[period]["total"] += balance

        result = list(transformed_data.values())
        columns = [{
            'dataField': card['creditCardId'],
            'caption': card['creditCardName'],
            'dataType': 'string'
        } for card in cards]

        return {
            'success': True,
            'history': {
                'periods': result,
                'columns': columns
            }
        }

    def __get_bill_history_aggregated(self, history):
        """
        :Name: get_bill_history_aggregated
        :Created by: Lucas Penha de Moura - 08/09/2022
        :Edited by:

        Explicit params:
        :param history: The complete queryset of history

        Implicit params (passed in the class instance or set by other functions):
        self.owner: the owner of the cards (logged user)

        Get the credit card expenses from all users cards by period
        """
        history = history.values('period') \
            .annotate(balance=Sum('amount') * -1)
        average = sum(item['balance'] for item in history) / len(history) if history else 0

        response = {
            'success': True,
            'average': average,
            'goal': 2300,
            'history': list(history),
        }

        return response
