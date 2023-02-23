import requests
from django.utils import timezone
import json
import BO.integration.integration
import finance.models


class Vat(BO.integration.integration.Integration):
    """
    :Name: VatRate
    :Description: Get the exchange rate from VAT Comply API
    :Created by: Lucas Penha de Moura - 24/08/2022
    :Edited by:

        VAT Comply documentation:
            https://www.vatcomply.com/documentation
    """

    def __init__(self):
        super().__init__(service='vat')
        self.base_url = 'https://api.vatcomply.com'

    def get_rate(self, base='BRL', date=timezone.localdate()):
        pass

    def get_currency(self):
        """
        :Name: VatRate
        :Description: Get currency list from VAT Comply API and update information in database
                        Set to execute once every six months
        :Created by: Lucas Penha de Moura - 22/02/2023
        :Edited by:
        """
        # TODO: modificar para usar integration!!
        # TODO: ver erro do self.url
        self.url = self.base_url + '/currencies'

        self.get()
        response = json.loads(self.response)

        current_currencies = finance.models.Currency.objects.values_list('id', flat=True)
        new_currency_list = []
        for key, value in response.items():
            if key not in list(current_currencies):
                new_currency = finance.models.Currency(
                    id=key,
                    name=value['name'],
                    symbol=value['symbol']
                )
                new_currency_list.append(new_currency)
        finance.models.Currency.objects.bulk_create(new_currency_list)

        return response
