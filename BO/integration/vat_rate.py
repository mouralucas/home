import requests
from django.utils import timezone
import json


class VatRate:
    """
    :Name: VatRate
    :Description: Get the exchange rate from VAT Comply API
    :Created by: Lucas Penha de Moura - 24/08/2022
    :Edited by:

        VAT Comply documentation:
            https://www.vatcomply.com/documentation
    """

    def __int__(self):
        self.url = 'https://api.vatcomply.com'

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
        endpoint = 'https://api.vatcomply.com' + '/currencies'

        response = requests.get(endpoint)
        response = json.loads(response.text)
        return response
