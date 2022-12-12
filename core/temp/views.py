from rest_framework.views import APIView

import BO.conexao_db.conexao
import finance.models


class MigrateFaturaToBill(APIView):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        bills_old = 'select * from finance.creditcard_bill order by id'
        bills_new = finance.models.CreditCardBill.objects.all()


        sql_alchemy.buscar(query=sql)
        faturas = sql_alchemy.get_dict()

        bill_list = []


        finance.models.CreditCardBill.objects.bulk_create(bill_list)

        print('')

