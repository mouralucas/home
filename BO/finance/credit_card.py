from django.db.models import Case, When, Value, CharField, F
from django.utils.translation import gettext_lazy as _
import util.datetime
import finance.models


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
        credit_cards = finance.models.CreditCard.objects.values('id', 'name', 'description', 'dat_closing', 'dat_due').active() \
            .annotate(nm_status=Case(When(status=True, then=Value(_('Ativo'))),
                                     default=Value(_('Cancelado')),
                                     output_field=CharField())).order_by('-status', 'id')

        response = {
            'status': True,
            'description': None,
            'quantity': len(credit_cards),
            'credit_cards': list(credit_cards),
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
            filters['period'] = self.period

            if self.credit_card_id:
                filters['credit_card_id'] = self.credit_card_id

        bills = finance.models.CreditCardBill.objects \
            .values('id', 'period', 'dat_purchase', 'dat_payment',
                    'installment', 'tot_installment', 'description') \
            .filter(**filters) \
            .annotate(amount=F('amount'),
                      credit_card_id=F('credit_card_id'),
                      nm_credit_card=F('credit_card__name'),
                      category_id=F('category_id'),
                      nm_category=F('category__description'),
                      datCreated=F('dat_created'),
                      datLastEdited=F('dat_last_edited')
                      ).order_by('-dat_purchase', '-dat_created')

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
        bill.dat_payment = dat_pagamento_date
        bill.dat_purchase = util.datetime.date_to_datetime(self.dat_purchase, output_format='%Y-%m-%d')

        # Amounts
        bill.amount = float(self.amount) * -1
        bill.amount_absolute = float(self.amount)
        bill.amount_total = self.amount  # TODO: modificar para adicionar o valor total de compras parceladas
        bill.amount_currency = float(self.amount) * -1
        bill.price_currency_dollar = self.price_currency_dollar
        bill.price_dollar = 1

        bill.currency_id = self.currency_id
        bill.category_id = self.category_id

        bill.installment = 1
        bill.tot_installment = self.tot_installment
        bill.description = self.description

        bill.is_validated = True

        bill.cash_flow = 'OUTGOING'

        bill.owner_id = self.owner

        bill.save(request_=request)

        response = {
            'success': True
        }

        return response
