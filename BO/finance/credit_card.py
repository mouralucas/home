from django.db.models import Case, When, Value, CharField, F

import finance.models


class CreditCard:
    def __init__(self, credit_card_id=None, period=None, owner=None):
        self.credit_card_id = credit_card_id
        self.period = period
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
            .annotate(nm_status=Case(When(status=True, then=Value('Ativo')),
                                     default=Value('Cancelado'),
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
