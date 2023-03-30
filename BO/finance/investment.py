from django.db.models import F

import finance.models


class Investment:
    def __init__(self):
        pass

    def get_investment(self):
        investments = finance.models.Investment.objects.values('pk', 'name', 'description', 'amount', 'price',
                                                               'date', 'dat_maturity', 'interest_rate', 'interest_index') \
            .annotate(id=F('pk'),
                      nm_custodian=F('custodian__name'),
                      id_custodian=F('custodian_id')).order_by('-date')

        response = {
            'success': True,
            'description': None,
            'investment': list(investments)
        }

        return response
