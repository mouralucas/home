import finance.models
from service.finance.finance import Finance


class Core(Finance):
    def __init__(self, category_id=None):
        super().__init__(category_id=category_id)

    def get_expense(self):
        """
        :Name: get_expense
        :Description: get the list of expenses based on filters
        :Created by: Lucas Penha de Moura - 13/10/2023
        :Edited by:

        Explicit params:
        None

        Implicit params (passed in the class instance or set by other functions):
        self.category_id: Category id

        Return: the list of saved accounts
        """
        statement = finance.models.AccountStatement.objects.filter(category_id=self.category_id)
        bill = finance.models.CreditCardBill.objects.filter(category_id=self.category_id)
