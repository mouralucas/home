import BO.finance.finance
import finance.models


class Account(BO.finance.finance.Finance):
    def __init__(self, owner=None):
        super().__init__(owner=owner)
        pass

    def get_accounts(self):
        """
        :Name: get_bank_accounts
        :Description: get the list of accounts
        :Created by: Lucas Penha de Moura - 02/10/2022
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        None

        Return: the list of saved accounts
        """
        bank_accounts = finance.models.Account.objects \
            .values('id', 'nickname', 'branch_formatted', 'account_number_formatted', 'dat_open', 'dat_close').filter(owner=self.owner).active()

        response = {
            'status': True,
            'description': None,
            'quantity': len(bank_accounts),
            'accounts': list(bank_accounts),
        }

        return response
