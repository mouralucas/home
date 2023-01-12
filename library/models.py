import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models


class Serie(core.models.Log):
    # nome = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    nm_original = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_country')

    class Meta:
        db_table = 'library"."serie'


class Collection(core.models.Log):
    # Agrupamento de itens que não necessariamente é uma série,
    # Pode incluir, por exemplo, duas impressões de um mesmo mangá em formatos diferentes
    name = models.CharField(max_length=250, null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'library"."collection'


class Publisher(core.models.Log):
    name = models.CharField(max_length=250, null=True)
    description = models.TextField(null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_country')
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'library"."publisher'


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
    cover = models.FileField(null=True, default='library/item/cover/no_cover.png')
    volume = models.IntegerField(null=True)
    publisher = models.ForeignKey('library.Publisher', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_publisher')
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

    summary = models.TextField(null=True)
    observation = models.TextField(null=True)

    origin = models.CharField(max_length=50, default='SYSTEM', null=True)

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


class ItemStatus(core.models.Log):
    log_status = models.ForeignKey('core.Status', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_status')
    item = models.ForeignKey('library.Item', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_item')
    date = models.DateField(null=True)

    class Meta:
        db_table = 'library"."item_logstatus'


class Reading(core.models.Log):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, null=True)
    item = models.ForeignKey('library.Item', on_delete=models.DO_NOTHING)
    dat_start = models.DateField()
    dat_end = models.DateField(null=True)
    is_dropped = models.BooleanField(default=False)

    class Meta:
        db_table = 'library"."reading'


class ReadingProgress(core.models.Log):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    reading = models.ForeignKey('library.Reading', on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    page = models.IntegerField(null=True)
    percentage = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    class Meta:
        db_table = 'library"."reading_progress'
