import time
import uuid

from compositefk.fields import CompositeForeignKey
from django.apps import apps
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=True)

    def disable(self, request_=None):
        user = request_.user.pk if request_ is not None else None
        qs = self.update(status=False, deleted_by=user, dat_deleted=timezone.now())
        return qs


class CustomManager(models.Manager):
    def queryset(self):
        return CustomQuerySet(self.model)

    def get_queryset(self):
        ini = time.time()
        qs = self.queryset()
        fim = time.time()
        tempo = 1
        try:
            if 0 < tempo < fim - ini:
                query = apps.get_model('log', BANCO.capitalize() + 'Query')
                query(
                    time=fim - ini,
                    query=str(qs.query)
                ).save()
        except Exception as e:
            print(e)
            pass

        return qs

    def active(self):
        return self.get_queryset().active()

    def disable(self, request_=None):
        return self.get_queryset().disable(request_=request_)


class Log(models.Model):
    normal_objects = models.Manager()
    objects = CustomManager()

    status = models.BooleanField(null=True, default=True)

    created_by = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_created_by')
    last_edited_by = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_last_edit_by')
    deleted_by = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_deleted_by')

    dat_created = models.DateTimeField(null=True, blank=True)
    dat_last_edited = models.DateTimeField(null=True, blank=True)
    dat_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True
        abstract = True

    def save(self, request_=None, is_update=True, *args, **kwargs):
        """
        :Name: logout
        :Created by: Lucas Penha de Moura - 07/08/2022
        :Edited by:

        Explicit params:
        :param request_: the request body
        :param is_update: if true add/update the last_edited_by and dat_last_edited fields

        Implicit params (passed in the class instance or set by other functions):
        None

        Create the created_by/last_edited_by and corresponding dates logs
        """
        if not self.dat_created:
            self.created_by = request_.user if request_ else None
            self.dat_created = timezone.now()
        elif is_update:
            self.last_edited_by = request_.user if request_ else None
            self.dat_last_edited = timezone.now()

        super(Log, self).save(*args, **kwargs)


class Person(Log):
    """
    :Name: Person
    :Description:
    :Created by: Lucas Penha de Moura - 14/08/2022
    :Edited by:
    """

    class IdTypes(models.TextChoices):
        CPF = ('cpf', _('CPF'))
        PASSPORT = ('passport', _('Passaporte'))

    class SexTypes(models.TextChoices):
        MALE = ('male', _('Masculino'))
        FEMALE = ('female', _('Feminino'))
        OTHER = ('other', _('Outro'))
        NO_RESPONSE = ('no_response', _('Prefiro não responder'))

    nm_full = models.CharField(_('Nome completo'), max_length=200, null=True)
    nm_first = models.CharField(_('Primeiro nome'), max_length=200, null=True)
    nm_last = models.CharField(_('Último nome'), max_length=200, null=True)

    person_id = models.BigIntegerField(_('Identification of the person (id number, passport, etc)'), unique=True)
    person_id_formatted = models.CharField(_('Formatted string of the person id'), max_length=20, null=True)

    id_type = models.CharField(max_length=100, choices=IdTypes.choices, default=IdTypes.CPF, null=True)

    dat_birth = models.DateField(null=True)
    image = models.FileField(upload_to='account/images/person/', default='account/images/person/default.svg', null=True)

    nm_mother = models.CharField(max_length=200, null=True)
    nm_father = models.CharField(max_length=200, null=True)

    email = models.EmailField(max_length=200, null=True)

    sex = models.CharField(max_length=50, choices=SexTypes.choices, default=SexTypes.NO_RESPONSE)

    account = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING)
    hash = models.UUIDField(default=uuid.uuid4)

    class Meta(Log.Meta):
        abstract = True


class PersonContact(models.Model):
    class ContactType(models.TextChoices):
        EMAIL = ('email', _('e-mail'))
        CELL = ('cellphone', _('Celular'))
        PHONE = ('phone', _('Telefone'))

    type = models.TextField(max_length=50, choices=ContactType.choices)
    raw_value = models.CharField(max_length=100, help_text='The value entered by user')
    formatted_value = models.CharField(max_length=100, help_text='The value formatted by the system, when applicable')

    class Meta(Log.Meta):
        abstract = True


class UF(Log):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=True)
    nm_abrev = models.CharField(max_length=2, null=True)
    cep_faixa_ini = models.CharField(max_length=80, null=True)
    cep_faixa_fim = models.CharField(max_length=80, null=True)

    class Meta(Log.Meta):
        db_table = 'public"."uf'


class State(Log):
    name = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=2, null=True)
    postal_code_ini = models.CharField(max_length=80, null=True)
    postal_code_fim = models.CharField(max_length=80, null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'public"."state'


class City(Log):
    id = models.CharField(max_length=100, primary_key=True)
    state = models.ForeignKey('core.State', on_delete=models.DO_NOTHING, null=True)
    nome = models.CharField(max_length=200)
    cep_faixa_ini = models.CharField(max_length=80, null=True)
    cep_faixa_fim = models.CharField(max_length=80, null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'public"."city'


class Tipo(Log):
    codigo = models.CharField(max_length=200, null=True)
    informacao = models.CharField(max_length=500, null=True)
    tipo = models.CharField(max_length=200, null=True)
    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)
    ordem = models.IntegerField(null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'public"."tipo'
        unique_together = ('codigo', 'tipo')


class Status(Log):
    class StatusTypes(models.TextChoices):
        LIBRARY_ITEM = ('library_item', _('Itens de Biblioteca'))
        LIBRARY_READING = 'library_reading', _('Status de leitura de item')

    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    order = models.IntegerField(null=True)
    image = models.FileField(upload_to='core/status', default='core/status/padrao.png', null=True)

    type = models.CharField(max_length=50, choices=StatusTypes.choices, null=True)

    # TODO: criar agrupamento e tirar relação com a tipo
    grupo_codigo = models.CharField(null=True, max_length=200)
    grupo_tipo = models.CharField(null=True, max_length=200, default='STATUS.GRUPO')
    grupo = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='status_grupo', to_fields={
        "codigo": "grupo_codigo",
        "tipo": "grupo_tipo"
    })

    class Meta:
        db_table = 'public"."status'


class Module(Log):
    id = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    father = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'public"."module'


class Category(Log):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=500)
    comments = models.TextField(null=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    module = models.ForeignKey('core.Module', on_delete=models.DO_NOTHING, null=True)
    order = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    is_default = models.BooleanField(default=False)
    owner = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, help_text='Category created by the user')

    class Meta:
        db_table = 'public"."category'


class Language(Log):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=10, null=True, help_text=_('Exemplo: pt-br'))

    class Meta:
        db_table = 'public"."language'


class Country(Log):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=250, null=True)
    continent = models.CharField(max_length=5, null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'public"."country'


class Region(Log):
    """
    Tabela que identifica os estados por pais, inclui os estados brasileiros, que já estão definidos em UF
    Para estados brasileiros usar UF por conter informações mais completas
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=250, null=True)
    local_code = models.CharField(max_length=50)
    continent = models.CharField(max_length=5, null=True)
    country = models.ForeignKey('core.Country', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'public"."country_region'


class SystemLanguages(Log):
    # Tabela que será usada para sistema multi-idioma
    # Contará com tabela auxiliar para registrar id_texto, id_idioma, texto_base,
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'public"."system_language'


class DynamicTextTranslation(Log):
    # Texto sem parent_id indica o idioma base, todos os filhos significam traduções
    # O id dessa tabela deverá ficar na tabela com texto dinâmico, quando procurar por outro idioma diferente do português buscar pelo parent_id + language_id, senão por id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    language = models.ForeignKey('core.SystemLanguages', on_delete=models.DO_NOTHING)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'public"."dynamic_text_translate'


# Choices available throughout the project
class GenderTypes(models.TextChoices):
    MALE = ('male', _('Masculino'))
    FEMALE = ('female', _('Feminino'))
    OTHER = ('other', _('Outro'))
    NO_RESPONSE = ('no_response', _('Prefiro não responder'))


class CurrencyTypes(models.TextChoices):
    REAL = ('BRL', _('R$ - Real'))
    EURO = ('EUR', _('€ - Euro'))
    DOLAR = ('USD', _('$ - Dólar'))
    CK_CROW = ('CZK', _('Kč - Coroa Tcheca'))

