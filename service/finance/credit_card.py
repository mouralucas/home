from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _

import finance.models
import util.datetime


class CreditCard:
    def __init__(self, mes=None, ano=None, statement_id=None, bill_id=None, period=None, account_id=None, credit_card_id=None, amount=None,
                 amount_currency=None, price_currency_dollar=None, vlr_moeda=None, amount_tax=None, installment=None, tot_installment=None,
                 dat_purchase=None, dat_payment=None,
                 description=None, category_id=None, currency_id=None, price_dollar=None, owner=None):
        self.statement_id = statement_id
        self.bill_id = bill_id
        self.period = period
        self.amount = amount
        self.amount_currency = amount_currency
        self.price_currency_dollar = price_currency_dollar
        self.vlr_moeda = vlr_moeda
        self.amount_tax = amount_tax
        self.instalment = installment
        self.tot_installment = tot_installment
        self.dat_purchase = dat_purchase
        self.dat_payment = dat_payment
        self.description = description
        self.category_id = category_id
        self.account_id = account_id
        self.credit_card_id = credit_card_id
        self.currency_id = currency_id
        self.owner = owner

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
        credit_cards = finance.models.CreditCard.objects.values('id', 'name', 'description', 'dat_closing', 'dat_due').active().order_by('-status', 'id')

        response = {
            'status': True,
            'description': None,
            'quantity': len(credit_cards),
            'creditCards': list(credit_cards),
        }

        return response

    def get_bill(self, credit_card_bill_id=None):
        filters = {
            'owner_id': self.owner
        }
        if credit_card_bill_id:
            # bills = bills.filter(id=credit_card_bill_id).first()
            filters['id'] = credit_card_bill_id

        else:
            filters['period'] = 202310

            if self.credit_card_id:
                filters['credit_card_id'] = self.credit_card_id

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
            'status': True,
            'bill': list(bills) if not credit_card_bill_id else bills
        }

        return response

    def set_bill(self, request=None):
        if not self.dat_purchase or not self.amount or not self.category_id or not self.credit_card_id:
            response = {
                'status': False,
                'description': _('Todos os parâmetros são obrigatórios')
            }
            return response

        if self.bill_id:
            bill = finance.models.CreditCardBill.objects.filter(pk=self.bill_id).first()
        else:
            bill = finance.models.CreditCardBill()

        # Não modificado
        dat_pagamento_date = util.datetime.date_to_datetime(self.dat_payment, output_format='%Y-%m-%d')
        referencia_ano = dat_pagamento_date.year
        referencia_mes = dat_pagamento_date.month
        self.period = referencia_ano * 100 + referencia_mes

        bill.credit_card_id = self.credit_card_id
        # Dates
        bill.period = self.period
        bill.payment_at = dat_pagamento_date
        bill.purchase_at = util.datetime.date_to_datetime(self.dat_purchase, output_format='%Y-%m-%d')

        # Amounts
        bill.amount = float(self.amount) * -1
        bill.amount_absolute = float(self.amount)
        bill.amount_total = self.amount  # TODO: modificar para adicionar o valor total de compras parceladas
        bill.amount_reference = float(self.amount) * -1  # vai vir da tela
        bill.dollar_currency_quote = self.price_currency_dollar  # vai vir da tela
        bill.dollar_quote = 1  # vai vir da tela

        bill.currency_id = self.currency_id
        bill.category_id = self.category_id

        bill.installment = 1  # vai vir da tela
        bill.tot_installment = self.tot_installment  # vai vir da tela
        bill.description = self.description

        bill.is_validated = True

        bill.cash_flow = 'OUTGOING'  # vai vir da tela

        bill.currency_reference_id = 'BRL'  # Vai vir da tela

        bill.owner_id = self.owner

        bill.save(request_=request)

        response = {
            'success': True
        }

        return response

    def get_bill_history(self, history_type, start_at, end_at):
        if history_type == 'aggregated':
            return self.__get_bill_history_aggregated(start_at=start_at, end_at=end_at)

        if history_type == 'byCard':
            return self.__get_bill_history_card(start_at=start_at, end_at=end_at)

    def __get_bill_history_card(self, start_at, end_at):
        """
        :Name: get_bill_history_aggregated
        :Created by: Lucas Penha de Moura - 20/10/2023
        :Edited by:

        Explicit params:
        :param start_at: Start period
        :param end_at: End period

        Implicit params (passed in the class instance or set by other functions):
        self.owner: the owner of the cards (logged user)

        Get the credit card expenses from all users cards by period/card
        """
        filters = {
            'owner_id': self.owner,
            'period__range': (start_at, end_at)
        }

        history = finance.models.CreditCardBill.objects.values('period', 'credit_card_id') \
            .annotate(balance=Sum('amount') * -1).filter(**filters).order_by('period')

        transformed_data = {}

        for item in history:
            period = item["period"]
            card_id = item["credit_card_id"]
            balance = item["balance"]

            if period not in transformed_data:
                transformed_data[period] = {
                    "period": period,
                    "totalByCard": {},
                    "total": 0,
                    "columns": []
                }

            if card_id not in transformed_data[period]["columns"]:
                transformed_data[period]["columns"].append(card_id)

            transformed_data[period]["totalByCard"][card_id] = balance
            transformed_data[period]["total"] += balance

        result = list(transformed_data.values())

        return {
            'success': True,
            'history': result
        }

    def __get_bill_history_aggregated(self, start_at, end_at):
        """
        :Name: get_bill_history_aggregated
        :Created by: Lucas Penha de Moura - 08/09/2022
        :Edited by:

        Explicit params:
        :param start_at: Start period
        :param end_at: End period

        Implicit params (passed in the class instance or set by other functions):
        self.owner: the owner of the cards (logged user)

        Get the credit card expenses from all users cards by period
        """
        filters = {
            'owner_id': self.owner,
            'period__range': (start_at, end_at)
        }

        history = finance.models.CreditCardBill.objects.values('period') \
            .annotate(
            total_amount=Sum('amount'),
            total_amount_absolute=Sum('amount_absolute'),
            balance=Sum('amount') * -1
        ).filter(**filters).order_by('period')

        average = sum(item['total_amount_absolute'] for item in history) / len(history) if history else 0

        response = {
            'success': True,
            'average': average,
            'goal': 2300,
            'history': list(history),
        }

        return response
