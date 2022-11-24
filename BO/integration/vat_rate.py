from django.utils import timezone

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
        pass

    def get_rate(self, base='BRL', date=timezone.localdate()):
        pass
