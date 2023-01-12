from rest_framework.views import APIView

import BO.conexao_db.conexao
import finance.models
import library.models


class MigrateFaturaToBill(APIView):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        bills_old = 'select * from finance.creditcard_bill order by id'
        bills_new = finance.models.CreditCardBill.objects.values('id', 'dat_created', 'dat_purchase', 'amount')

        sql_alchemy.buscar(query=sql)
        faturas = sql_alchemy.get_dict()

        bill_list = []

        finance.models.CreditCardBill.objects.bulk_create(bill_list)

        print('')


class UpdateDateTime(APIView):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home')

        sql = 'select * from library.serie order by id'
        sql_alchemy.buscar(query=sql)
        old_references = sql_alchemy.get_dict()
        new_references = library.models.Serie.objects.order_by('id')

        for idx, i in enumerate(new_references):
            try:
                i.dat_created = next(item['dat_created'] for item in old_references if item["id"] == i.id)
            except Exception as e:
                print(e, idx)
        library.models.Serie.objects.bulk_update(new_references, ['dat_created'])

        print(old_references)
