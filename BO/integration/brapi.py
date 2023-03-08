import BO.integration.integration


class Brapi(BO.integration.integration.Integration):
    """
    :Name: Brpai
    :Description: Get information from stock market
    :Created by: Lucas Penha de Moura - 07/03/2023
    :Edited by:

        Brapi documentation:
            https://brapi.dev/docs
    """
    def __init__(self):
        super(Brapi, self).__init__(service='brapi')
        self.base_url = 'https://brapi.dev/'

    def get_tiker_history(self):
        pass

    def get_prime_rate(self, country='brazil'):
        self.url = self.base_url + '/api/v2/prime-rate'
        self.body = {
            'country': country
        }

