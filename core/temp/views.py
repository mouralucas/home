from django.views import View

import BO.conexao_db.conexao
import finance.models
import library.models


class MigrateFaturaToBill(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from financeiro.fatura order by id'

        sql_alchemy.buscar(query=sql)
        faturas = sql_alchemy.get_dict()

        bill_list = []
        for fatura in faturas:
            bill = finance.models.CreditCardBill()
            bill.dat_created = fatura['dat_insercao']
            bill.status = fatura['status']
            bill.id = fatura['id']
            bill.credit_card_id = fatura['cartao_credito_id']
            bill.reference = fatura['referencia']
            bill.dat_payment = fatura['dat_pagamento']
            bill.dat_purchase = fatura['dat_compra']
            bill.amount = fatura['valor']
            bill.category_id = fatura['categoria_id']
            bill.currency = fatura['currency']
            bill.amount_currency = fatura['vlr_original']
            bill.price_dollar = fatura['vlr_dolar']
            bill.price_currency_dollar = fatura['vlr_moeda']
            bill.tax = fatura['iof']
            bill.stallment = fatura['nr_parcela']
            bill.tot_stallment = fatura['tot_parcela']
            bill.is_stallment = fatura['is_parcela']
            bill.father_id = fatura['registro_pai_id']
            bill.description = fatura['descricao']
            bill.origin = fatura['origem']
            bill.is_validated = True

            bill_list.append(bill)

        finance.models.CreditCardBill.objects.bulk_create(bill_list)

        print('')


class MigrateExtratoToStatement(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from financeiro.extrato order by id'

        sql_alchemy.buscar(query=sql)
        extratos = sql_alchemy.get_dict()

        statement_list = []
        for extrato in extratos:
            statement = finance.models.BankStatement()
            statement.dat_created = extrato['dat_insercao']
            statement.status = extrato['status']

            statement.id = extrato['id']
            statement.account_id = extrato['conta_id']
            statement.reference = extrato['referencia']
            statement.amount = extrato['valor']
            statement.dat_purchase = extrato['dat_compra']
            statement.category_id = extrato['categoria_id']
            statement.description = extrato['descricao']
            statement_list.append(statement)

        finance.models.BankStatement.objects.bulk_create(statement_list)
        print('')

class MigrateAutorToAuthor(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from biblioteca.autor order by id'

        sql_alchemy.buscar(query=sql)
        autores = sql_alchemy.get_dict()

        author_list = []
        for autor in autores:
            author = library.models.Author()
            author.id = autor['id']
            author.dat_created = autor['dat_insercao']
            author.dat_last_edited = autor['dat_edicao']
            author.created_by_id = 1
            author.status = autor['status']
            author.nm_full = autor['nm_completo']
            author.nm_first = autor['nome']
            author.nm_last = autor['sobrenome']
            author.dat_birth = autor['dat_nascimento']
            author.description = autor['descricao']
            author.is_translator = autor['is_tradutor']
            # author.language_id = autor['idioma_id'].upper().strip() if autor['idioma_id'] else None
            author.country_id = autor['pais_id']
            author_list.append(author)

        library.models.Author.objects.bulk_create(author_list)


class MigrateColecaoToCollectiontem(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from biblioteca.colecao order by id'

        sql_alchemy.buscar(query=sql)
        colecoes = sql_alchemy.get_dict()

        collection_list = []
        for colecao in colecoes:
            collection = library.models.Collection()
            collection.id = colecao['id']
            collection.dat_created = colecao['dat_insercao']
            collection.created_by_id = 1
            collection.status = colecao['status']
            collection.name = colecao['nome']
            collection.description = colecao['descricao']
            collection_list.append(collection)

        library.models.Collection.objects.bulk_create(collection_list)
        print()


class MigrateEdtoraToPublisher(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from biblioteca.editora order by id'

        sql_alchemy.buscar(query=sql)
        editoras = sql_alchemy.get_dict()

        publisher_list = []
        for editora in editoras:
            publisher = library.models.Publisher()
            publisher.id = editora['id']
            publisher.dat_created = editora['dat_insercao']
            publisher.dat_last_edited = editora['dat_edicao']
            publisher.created_by_id = 1
            publisher.status = editora['status']
            publisher.name = editora['nome']
            publisher.description = editora['descricao']
            publisher.country_id = editora['pais_id']
            publisher_list.append(publisher)

        library.models.Publisher.objects.bulk_create(publisher_list)
        print()

class MigrateSerieToSerie(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from biblioteca.serie order by id'

        sql_alchemy.buscar(query=sql)
        series = sql_alchemy.get_dict()

        serie_list = []
        for serie in series:
            serie_new = library.models.Serie()
            serie_new.id = serie['id']
            serie_new.dat_created = serie['dat_insercao']
            serie_new.dat_last_edited = serie['dat_edicao']
            serie_new.created_by_id = 1
            serie_new.status = serie['status']
            serie_new.name = serie['name']
            serie_new.nm_original = serie['nm_original']
            serie_new.description = serie['description']
            serie_new.country_id = serie['country_id']
            serie_list.append(serie_new)

        library.models.Serie.objects.bulk_create(serie_list)
        print()

class MigrateLivroToItem(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from biblioteca.livro order by id'

        sql_alchemy.buscar(query=sql)
        livros = sql_alchemy.get_dict()

        item_list = []
        for livro in livros:
            item = library.models.Item()
