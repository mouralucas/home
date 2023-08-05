from service.integration.integration import Integration
import pandas as pd


class BancoCentralAPI(Integration):
    """
    :Name: format_data
    :Description: Format the date into the requestd format
    :Created by: Lucas Penha de Moura - 03/04/2020
    :Edited by:

    Fetch and persist data from SGS into database
    Data codes:
    11	    Taxa de juros - Selic
    432     Taxa de juros - Meta Selic definida pelo Copom
    1178    Taxa de juros - Selic anualizada base 252
    4389	Taxa de juros - CDI anualizada base 252

    Integration with the Banco Central do Brasil open data API
    """
    def __init__(self, service):
        super().__init__(service)
        self.url_bcdata = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados?formato=json&dataInicial=01/01/2023&dataFinal=31/12/2023'

    def historical_data_selic_integration(self):
        juros_cdi = pd.read_json(self.url_bcdata)

    def daily_selic_update(self):
        pass