from django.db.models import F, Sum

import finance.models


class Investment:
    def __init__(self):
        pass

    def get_investment(self):
        filters = {}

        investments = finance.models.Investment.objects.values('pk', 'name', 'description', 'amount', 'price',
                                                               'date', 'dat_maturity', 'interest_rate', 'interest_index') \
            .annotate(id=F('pk'),
                      nm_custodian=F('custodian__name'),
                      id_custodian=F('custodian_id'),
                      id_type=F('type_id'),
                      nm_type=F('type__name')).order_by('-date').active().filter(**filters)

        response = {
            'success': True,
            'description': None,
            'investment': list(investments)
        }

        return response

    def get_proportion(self):
        proportion = finance.models.Investment.objects.values('type__name').annotate(total=Sum('amount'))

        response = {
            'success': True,
            'investment_proportion': list(proportion)
        }

        return response
