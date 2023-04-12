from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _

import finance.models


class Investment:
    def __init__(self, investment_id=None):
        self.investment_id = investment_id

    def set_investment(self, parent_id=None, name=None, date=None, quantity=None, price=None, amount=None,
                       cash_flow=None, interest_rate=None, interest_index=None, investment_type_id=None, dat_maturity=None,
                       custodian_id=None, owner_id=None, request=None):

        # TODO: veririficar possível forma de dividir o cadsatro em dois, no primeiro nível só contar informações do investimento, sem valores (parent), no segundo os detalhes mais o valor (child)

        amount = amount * -1 if cash_flow == 'OUTGOING' else amount

        investment = finance.models.Investment()

        if not parent_id:
            # The first entry of the investment contains 2 rows, the first (without parent_id) is the total of the investment
            #   Any other row (with parent_id) representes each transaction in the investment, and changes the amount of the parent
            investment.name = name
            investment.date = date
            investment.quantity = quantity
            investment.price = price
            investment.amount = amount
            investment.cash_flow = cash_flow
            investment.interest_rate = interest_rate
            investment.interest_index = interest_index
            investment.type_id = investment_type_id
            investment.dat_maturity = dat_maturity
            investment.custodian_id = custodian_id
            investment.owner_id = owner_id
            investment.save(request_=request)

            child_investment = finance.models.Investment.objects.filter(pk=investment.pk).first()
            child_investment.pk = None
            child_investment.parent_id = investment.pk
            child_investment.save(request_=request)

        else:
            parent_investment = finance.models.Investment.objects.filter(parent_id=parent_id).first()
            parent_investment.amount += amount
            parent_investment.save(request_=request)

            child_investment = finance.models.Investment()
            child_investment.name = name
            child_investment.date = date
            child_investment.quantity = quantity
            child_investment.price = price
            child_investment.amount = amount
            child_investment.cash_flow = cash_flow
            child_investment.interest_rate = interest_rate
            child_investment.interest_index = interest_index
            child_investment.type_id = investment_type_id
            child_investment.dat_maturity = dat_maturity
            child_investment.custodian_id = custodian_id
            child_investment.owner = owner_id

        response = {
            'success': True,
        }
        return response

    def get_investment(self):
        filters = {}

        if self.investment_id:
            filters['pk'] = self.investment_id

        investments = finance.models.Investment.objects.values('pk', 'name', 'description', 'amount', 'price', 'quantity',
                                                               'date', 'parent_id') \
            .annotate(id=F('pk'),
                      maturityDate=F('dat_maturity'),
                      interestRate=F('interest_rate'),
                      interestIndex=F('interest_index'),
                      custodianName=F('custodian__name'),
                      custodianId=F('custodian_id'),
                      investmentTypeId=F('type_id'),
                      investmentTypeName=F('type__name')).order_by('-date').active().filter(**filters)

        response = {
            'success': True,
            'description': None,
            'investment': list(investments) if not self.investment_id else investments.first()
        }

        return response

    def get_investment_statement(self):

        response = {
            'success': True,
        }

        return response

    def get_investment_type(self, show_mode):
        if show_mode not in ['all', 'father', 'child']:
            return {
                'status': False,
                'description': _('Show mode dever ser uma das três opções: all, father ou child')
            }

        filters = {}
        if show_mode != 'all':
            filters['parent_id__isnull'] = True if show_mode == 'father' else False

        investment_type = finance.models.InvestmentType.objects.values('id', 'name', 'description').filter(**filters).order_by('name')

        response = {
            'success': True,
            'description': None,
            'investment_type': list(investment_type)
        }

        return response

    def get_proportion(self):
        proportion = finance.models.Investment.objects.values('type__name').annotate(total=Sum('amount'))

        response = {
            'success': True,
            'investment_proportion': list(proportion)
        }

        return response
