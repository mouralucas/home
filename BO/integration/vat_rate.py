import json
from datetime import datetime

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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

    def get_currency_rate(self, base='USD', date=None):
        if datetime.strptime(date, '%Y-%m-%d') < datetime.strptime('2008-01-02', '%Y-%m-%d'):
            return {
                'success': False,
                'description': _('Não é possível buscar cotações anteriores a 02 de janeiro de 2008')
            }

        self.url = self.base_url + '/rates'
        self.params = {
            'date': date,
            'base': base
        }

        # TODO: adicionar validação por base, moeda e dia e buscar caso não encontre e adicionar if pra não adicionar caso já existe outra combinação no mesmo dia
        currency_rate = finance.models.CurrencyRate.objects.filter(date=date, base_id=base)
        wanted_currency_rates = finance.models.Currency.objects.values_list('id', flat=True).filter(is_shown=True)
        if not currency_rate:
            self.get()
            response = json.loads(self.response)

            rate_list = []
            for key, value in response['rates'].items():
                if key in wanted_currency_rates and base != key:
                    aux = finance.models.CurrencyRate(
                        date=date,
                        base_id=base,
                        currency_id=key,
                        price=value
                    )
                    rate_list.append(aux)
            finance.models.CurrencyRate.objects.bulk_create(rate_list)

            return {
                'success': True,
                'inserted_qtd': len(rate_list),
                'date': date,
                'base': base,
            }
        return {
            'success': False,
            'description': _('Conversão para a moeda base já cadastrada para a data {date}'.format(date=date))
        }

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
