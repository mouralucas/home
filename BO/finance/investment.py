from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _

import finance.models


class Investment:
    def __init__(self, investment_id=None):
        self.investment_id = investment_id

    def set_investment(self):
        # Set investment code
        response = self.get_investment()
        return response

    def get_investment(self):
        filters = {}

        if self.investment_id:
            filters['pk'] = self.investment_id

        investments = finance.models.Investment.objects.values('pk', 'name', 'description', 'amount', 'price', 'quantity',
                                                               'date') \
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
        invest = finance.models.InvestmentStatement.objects.values('id', 'investment__amount_invested', 'vlr_bruto', 'vlr_liquido', 'referencia') \
            .filter(reference=self.period).annotate(nm_investimento=F('aplicacao__nm_descritivo')).order_by('aplicacao__nm_descritivo')

        response = {
            'success': True,
            'investment_statement': list(invest)
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
