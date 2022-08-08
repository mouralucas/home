from itertools import chain

from compositefk.fields import CompositeForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models


class Serie(core.models.Log):
    # nome = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    nm_original = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_pais')

    class Meta:
        db_table = 'library"."serie'


# class Colecao(core.models.Log):
#     # Agrupamento de itens que não necessariamente é uma série,
#     # Pode incluir, por exemplo, duas impressões de um mesmo mangá em formatos diferentes
#     nome = models.CharField(max_length=250, null=True)
#     descricao = models.TextField(null=True)
#
#     class Meta:
#         db_table = u'"library\".\"colecao"'


class Collection(core.models.Log):
    # Agrupamento de itens que não necessariamente é uma série,
    # Pode incluir, por exemplo, duas impressões de um mesmo mangá em formatos diferentes
    name = models.CharField(max_length=250, null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'library"."collection'


# class Editora(core.models.Log):
#     nome = models.CharField(max_length=250, null=True)
#     descricao = models.TextField(null=True)
#     pais = models.ForeignKey('core.Pais', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_pais')
#
#     class Meta:
#         db_table = u'"library\".\"editora"'


class Publisher(core.models.Log):
    name = models.CharField(max_length=250, null=True)
    description = models.TextField(null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_country')

    class Meta:
        db_table = 'library"."publisher'


# class Autor(core.models.Log):
#     nome = models.CharField(max_length=250, null=True)
#     sobrenome = models.CharField(max_length=250, null=True)
#     nm_completo = models.CharField(max_length=500, null=True)
#     dat_nascimento = models.DateField(null=True)
#     descricao = models.TextField(null=True)
#     pais = models.ForeignKey('core.Pais', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_pais')
#     idioma = models.ForeignKey('core.Idioma', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_idioma')
#     is_tradutor = models.BooleanField(default=False, null=True)
#
#     class Meta:
#         db_table = u'"library\".\"autor"'


class Author(core.models.Log):
    nm_full = models.CharField(max_length=500, null=True)
    nm_first = models.CharField(max_length=250, null=True)
    nm_last = models.CharField(max_length=250, null=True)
    dat_birth = models.DateField(null=True)
    description = models.TextField(null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_country')
    language = models.ForeignKey('core.Language', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_language')
    is_translator = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'library"."author'


# class Livro(core.models.Log):
#     isbn = models.BigIntegerField(null=True)
#     isbn_form = models.CharField(max_length=100, null=True)
#     isbn10 = models.BigIntegerField(null=True)
#     isbn10_form = models.CharField(max_length=100, null=True)
#
#     titulo = models.CharField(max_length=500, null=True)
#     titulo_original = models.CharField(max_length=500, null=True)
#     subtitulo = models.CharField(max_length=500, null=True)
#     subtitulo_original = models.CharField(max_length=500, null=True)
#     paginas = models.IntegerField(null=True)
#     dat_lancamento = models.DateField(null=True)
#     dat_lancamento_original = models.DateField(null=True)
#     edicao = models.IntegerField(null=True)
#     serie = models.ForeignKey('library.Serie', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_serie')
#     idioma = models.ForeignKey('core.Idioma', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_idioma')
#     capa = models.FileField(null=True, default='library/item/capa/sem_capa.png')
#     volume = models.IntegerField(null=True)
#     editora = models.ForeignKey('library.Editora', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_editora')
#     autores = models.ManyToManyField('library.Autor', through='library.LivroAutor', related_name='%(app_label)s_%(class)s_livroautor')
#     autor_principal = models.ForeignKey('library.Autor', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_autor_principal', null=True)
#     # categoria = models.ManyToManyField('library.Categoria', through='library.LivroCategoria', related_name='%(app_label)s_%(class)s_livrocategoria')
#     colecao = models.ForeignKey('library.Colecao', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_livrocolecao', null=True)
#
#     formato_codigo = models.CharField(null=True, max_length=200)
#     formato_tipo = models.CharField(null=True, max_length=200, default='FORMATO.LIVRO')
#     formato = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_formato', to_fields={
#         "codigo": "formato_codigo",
#         "tipo": "formato_tipo"
#     }, help_text='Formato do livro (capa comum, hardcover, ebook, etc)')
#
#     # tipo (manga, livro, revista)
#     tipo_codigo = models.CharField(null=True, max_length=200)
#     tipo_tipo = models.CharField(null=True, max_length=200, default='TIPO.LIVRO')
#     tipo = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_tipo', to_fields={
#         "codigo": "tipo_codigo",
#         "tipo": "tipo_tipo"
#     }, help_text='Tipo de livro (livro, mangá, revista, etc')
#
#     ultimo_status = models.ForeignKey('core.Status', on_delete=models.DO_NOTHING, null=True)
#     dat_ultimo_status = models.DateField(null=True)
#     log_status = models.ManyToManyField('core.Status', through='library.LivroStatus', through_fields=('livro', 'log_status'), related_name='%(app_label)s_%(class)s_logstatus')
#     valor_capa = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#
#     dimensoes = models.CharField(max_length=50, null=True, help_text='Dimensões formatado em texto')
#     altura = models.DecimalField(max_digits=7, decimal_places=2, null=True, help_text='Em centímetros')
#     largura = models.DecimalField(max_digits=7, decimal_places=2, null=True, help_text='Em centímetros')
#     profundidade = models.DecimalField(max_digits=7, decimal_places=2, null=True, help_text='Em centímetros')
#
#     resumo = models.TextField(null=True)
#     observacoes = models.TextField(null=True)
#
#     origem_cadastro = models.CharField(max_length=50, default='SISTEMA', null=True)
#
#     def to_dict(self):
#         opts = self._meta
#         data = {}
#         for f in chain(opts.concrete_fields, opts.private_fields):
#             data[f.name] = f.value_from_object(self)
#
#         for f in opts.many_to_many:
#             data[f.name] = [i.pk for i in f.value_from_object(self)]
#         return data
#
#     class Meta:
#         db_table = u'"library\".\"livro"'


class Item(core.models.Log):
    class FormatType(models.TextChoices):
        HARDCOVER = ('hardcover', _('Capa Dura'))
        PAPERBACK = ('paperback', _('Capa comum'))
        EBOOK = ('ebook', _('e-Book'))
        HARDBACK = ('hardback', _('Hardback'))
        POCKET = ('pocket', _('Pocket'))

    class ItemType(models.TextChoices):
        BOOK = ('book', _('Livro'))
        MANGA = ('manga', _('Mangá'))

    isbn = models.BigIntegerField(null=True)
    isbn_formatted = models.CharField(max_length=100, null=True)
    isbn10 = models.BigIntegerField(null=True)
    isbn10_formatted = models.CharField(max_length=100, null=True)

    title = models.CharField(max_length=500, null=True)
    title_original = models.CharField(max_length=500, null=True)
    subtitle = models.CharField(max_length=500, null=True)
    subtitle_original = models.CharField(max_length=500, null=True)
    pages = models.IntegerField(null=True)
    dat_published = models.DateField(null=True)
    dat_published_original = models.DateField(null=True)
    edition = models.IntegerField(null=True)
    serie = models.ForeignKey('library.Serie', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_serie')
    language = models.ForeignKey('core.Language', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_language')
    cover = models.FileField(null=True, default='library/item/capa/sem_capa.png')
    volume = models.IntegerField(null=True)
    publisher = models.ForeignKey('library.Publisher', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_pubisher')
    authors = models.ManyToManyField('library.Author', through='library.ItemAuthor', related_name='%(app_label)s_%(class)s_authors')
    main_author = models.ForeignKey('library.Author', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_main_author', null=True)
    # category = models.ManyToManyField('library.Categoria', through='library.LivroCategoria', related_name='%(app_label)s_%(class)s_category')
    collection = models.ForeignKey('library.Collection', on_delete=models.DO_NOTHING, related_name='%(app_label)s_%(class)s_collection', null=True)

    format = models.CharField(max_length=30, choices=FormatType.choices, default=FormatType.PAPERBACK, null=True)
    type = models.CharField(max_length=30, choices=ItemType.choices)

    last_status = models.ForeignKey('core.Status', on_delete=models.DO_NOTHING, null=True)
    dat_last_status = models.DateField(null=True)
    log_status = models.ManyToManyField('core.Status', through='library.ItemStatus', through_fields=('item', 'log_status'), related_name='%(app_label)s_%(class)s_logstatus')
    cover_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    dimensions = models.CharField(max_length=50, null=True, help_text=_('Dimensões formatado em texto'))
    height = models.DecimalField(max_digits=7, decimal_places=2, null=True, help_text=_('Em centímetros'))
    width = models.DecimalField(max_digits=7, decimal_places=2, null=True, help_text=_('Em centímetros'))
    thickness = models.DecimalField(max_digits=7, decimal_places=2, null=True, help_text=_('Em centímetros'))

    resumo = models.TextField(null=True)
    observation = models.TextField(null=True)

    origem = models.CharField(max_length=50, default='SYSTEM', null=True)

    # def to_dict(self):
    #     opts = self._meta
    #     data = {}
    #     for f in chain(opts.concrete_fields, opts.private_fields):
    #         data[f.name] = f.value_from_object(self)
    #
    #     for f in opts.many_to_many:
    #         data[f.name] = [i.pk for i in f.value_from_object(self)]
    #     return data

    class Meta:
        db_table = 'library"."item'


class ItemAuthor(core.models.Log):
    item = models.ForeignKey('library.Item', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_item')
    author = models.ForeignKey('library.Author', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_author')
    is_main = models.BooleanField(default=True, null=True)
    is_translator = models.BooleanField(default=False, null=True)

    class Meta:
        unique_together = ['item', 'author']
        db_table = 'library"."item_author'


# class LivroAutor(core.models.Log):
#     livro = models.ForeignKey('library.Livro', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_livro')
#     autor = models.ForeignKey('library.Autor', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_autor')
#     is_principal = models.BooleanField(default=True, null=True)
#     is_tradutor = models.BooleanField(default=False, null=True)
#
#     class Meta:
#         unique_together = ['livro', 'autor']
#         db_table = u'"library\".\"livro_autor"'


# class LivroImagens(core.models.Log):
#     livro = models.ForeignKey('library.Livro', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_livro')
#     imagem = models.FileField(null=True)
#
#     class Meta:
#         db_table = u'"library\".\"livro_imagens"'


# class LivroStatus(core.models.Log):
#     log_status = models.ForeignKey('core.Status', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_status')
#     livro = models.ForeignKey('library.Livro', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_livro')
#     data = models.DateField(null=True)
#
#     class Meta:
#         db_table = u'"library\".\"livro_logstatus"'


class ItemStatus(core.models.Log):
    log_status = models.ForeignKey('core.Status', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_status')
    item = models.ForeignKey('library.Item', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_item')
    date = models.DateField(null=True)

    class Meta:
        db_table = 'library"."item_logstatus'


# class Categoria(core.models.Log):
#     nome = models.CharField(max_length=100, primary_key=True)
#     nm_descritivo = models.CharField(max_length=100, null=True)
#     descricao = models.CharField(max_length=500, null=True)
#
#     class Meta:
#         db_table = u'"library\".\"categoria"'


# class LivroCategoria(core.models.Log):
#     livro = models.ForeignKey('library.Livro', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_livro')
#     categoria = models.ForeignKey('library.Categoria', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_categoria')
#
#     class Meta:
#         db_table = u'"library\".\"livro_categoria"'


# class HistoricoLeitura(core.models.Log):
#     livro = models.ForeignKey('library.Livro', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_livro')
#     data = models.DateField(auto_now_add=True, null=True)
#     pagina = models.IntegerField(null=True)
#     porcentagem = models.DecimalField(max_digits=7, decimal_places=2, null=True)
#
#     class Meta:
#         db_table = u'"library\".\"livro_historicoleitura"'
