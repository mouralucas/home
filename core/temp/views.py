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
            if livro['formato_codigo'] == 'capa_comum':
                item_format = 'paperback'
            elif livro['formato_codigo'].lower() == 'pocket':
                item_format = 'pocket'
            elif livro['formato_codigo'] == 'hardback':
                item_format = 'hardback'
            elif livro['formato_codigo'] == 'ebook':
                item_format = 'ebook'
            elif livro['formato_codigo'] == 'hardcover':
                item_format = 'hardcover'
            else:
                item_format = None

            if livro['tipo_codigo'] == 'manga':
                item_type = 'manga'
            elif livro['tipo_codigo'] == 'livro':
                item_type = 'book'
            else:
                item_type = None

            item = library.models.Item()
            item.id = livro['id']
            item.dat_created = livro['dat_insercao']
            item.dat_last_edited = livro['dat_edicao']
            item.created_by_id = 1
            item.status = livro['status']

            item.isbn = livro['isbn']
            item.isbn_formatted = livro['isbn_form']
            item.isbn10 = livro['isbn10']
            item.isbn10_formatted = livro['isbn10_form']
            item.title = livro['titulo']
            item.title_original = livro['titulo_original']
            item.subtitle = livro['subtitulo']
            item.subtitle_original = livro['subtitulo_original']
            item.pages = livro['paginas']
            item.dat_published = livro['dat_lancamento']
            item.dat_published_original = livro['dat_lancamento_original']
            item.edition = livro['edicao']
            item.cover = livro['capa']
            item.volume = livro['volume']
            item.format = item_format
            item.type = item_type
            item.cover_price = livro['valor_capa']
            item.payed_price = livro['valor_pago']
            item.resumo = livro['resumo']
            item.publisher_id = livro['editora_id']
            item.language_id = livro['idioma_id'].upper() if livro['idioma_id'].upper() else None
            item.last_status_id = livro['ultimo_status_id']
            item.height = livro['altura']
            item.width = livro['largura']
            item.thickness = livro['profundidade']
            item.dimensions = livro['dimensoes']
            item.observation = livro['observacoes']
            item.origem = livro['origem_cadastro']
            item.serie_id = livro['serie_id']
            item.main_author_id = livro['autor_principal_id']
            item.collection_id = livro['colecao_id']
            item.dat_last_status = livro['dat_ultimo_status']

            item_list.append(item)

        library.models.Item.objects.bulk_create(item_list)


class MigrateLivroAutorToItemAuthor(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from biblioteca.livro_autor order by id'

        sql_alchemy.buscar(query=sql)
        livros_autores = sql_alchemy.get_dict()

        list = []
        for i in livros_autores:
            new_object = library.models.ItemAuthor()
            new_object.id = i['id']
            new_object.dat_created = i['dat_insercao']
            new_object.dat_last_edited = i['dat_edicao']
            new_object.created_by_id = 1
            new_object.status = i['status']

            new_object.is_main = i['is_principal']
            new_object.author_id = i['autor_id']
            new_object.item_id = i['livro_id']
            new_object.is_translator = i['is_tradutor']
            list.append(new_object)

        library.models.ItemAuthor.objects.bulk_create(list)
        print()

class MigrateLivroLogStatusrToItemLogStatus(View):
    def get(self, *args, **kwargs):
        sql_alchemy = BO.conexao_db.conexao.SqlAlchemy(database='home_beta')

        sql = 'select * from biblioteca.livro_logstatus order by id'

        sql_alchemy.buscar(query=sql)
        livros_logstatus = sql_alchemy.get_dict()

        list = []
        for i in livros_logstatus:
            new_object = library.models.ItemStatus()
            new_object.id = i['id']
            new_object.dat_created = i['dat_insercao']
            new_object.dat_last_edited = i['dat_edicao']
            new_object.created_by_id = 1
            new_object.status = i['status']

            new_object.item_id = i['livro_id']
            new_object.log_status_id = i['log_status_id']
            new_object.date = i['data']
            list.append(new_object)

        library.models.ItemStatus.objects.bulk_create(list)
        print()