import time

from compositefk.fields import CompositeForeignKey
from django.apps import apps
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# from core.util.core import Inteliger


class CustomQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=True)

    def desabilitar(self, request_=None):
        usuario = request_.user.pk if request_ is not None else None
        qs = self.update(status=False, usr_delete=usuario, dat_delete=timezone.now())
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

    def desabilitar(self, request_=None):
        return self.get_queryset().desabilitar(request_=request_)


class Log(models.Model):
    normal_objects = models.Manager()
    objects = CustomManager()

    status = models.BooleanField(null=True, default=True)

    created_by = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_created')
    last_edited_by = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_last_edit')
    deleted_by = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_deleted')

    dat_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dat_last_edited = models.DateTimeField(auto_now=True, null=True, blank=True)
    dat_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True
        abstract = True

    def save(self, request_=None, *args, **kwargs):
        if self.dat_created is None:
            # self.usr_insercao = request_.user.pk if request_ is not None else None
            self.dat_created = timezone.now()
            # self.origem_insercao_codigo = request_.user.tipo_codigo if request_ is not None and request_.user.pk is not None else None
            self.status = True
        else:
            # self.usr_edicao = request_.user.pk if request_ is not None else None
            self.dat_last_edited = timezone.now()
            # self.origem_edicao_codigo = request_.user.tipo_codigo if request_ is not None and request_.user.pk is not None else None

        super(Log, self).save(*args, **kwargs)

    # def desabilitar(self, request_=None, *args, **kwargs):
    #     self.status = False
    #     self.user = request_.user.pk if request_ is not None else None
    #     self.dat_delete = timezone.now()
    #     self.origem_delete_codigo = request_.user.tipo_codigo if request_ is not None and request_.user.pk is not None else None
    #     super(Log, self).save(*args, **kwargs)

    # def get_log(self):
    #     log = {
    #         'usr_insercao': None,
    #         'dat_insercao': self.dat_created,
    #         'usr_edicao': None,
    #         'dat_edicao': self.dat_last_edited,
    #         'usr_delete': None,
    #         'dat_delete': None,
    #     }
    #     if self.usr_insercao is not None:
    #         if self.origem_insercao_codigo == 'cliente':
    #             log['usr_insercao'] = apps.get_model('cliente', 'ClienteLogin').objects.all().filter(id=self.usr_insercao).first()
    #         elif self.origem_insercao_codigo == 'funcionario':
    #             log['usr_insercao'] = apps.get_model('funcionario', 'FuncionarioLogin').objects.all().filter(id=self.usr_insercao).first()
    #         elif self.origem_insercao_codigo == 'fornecedor':
    #             log['usr_insercao'] = apps.get_model('fornecedor', 'FornecedorLogin').objects.all().filter(id=self.usr_insercao).first()
    #         elif self.origem_insercao_codigo == 'api':
    #             log['usr_insercao'] = apps.get_model('api', 'ApiLogin').objects.all().filter(id=self.usr_insercao).first()
    #
    #     if self.usr_edicao is not None:
    #         if self.origem_edicao_codigo == 'cliente':
    #             log['usr_edicao'] = apps.get_model('cliente', 'ClienteLogin').objects.all().filter(id=self.usr_edicao).first()
    #         elif self.origem_edicao_codigo == 'funcionario':
    #             log['usr_edicao'] = apps.get_model('funcionario', 'FuncionarioLogin').objects.all().filter(id=self.usr_edicao).first()
    #         elif self.origem_edicao_codigo == 'fornecedor':
    #             log['usr_edicao'] = apps.get_model('fornecedor', 'FornecedorLogin').objects.all().filter(id=self.usr_edicao).first()
    #         elif self.origem_edicao_codigo == 'api':
    #             log['usr_edicao'] = apps.get_model('api', 'ApiLogin').objects.all().filter(id=self.usr_edicao).first()
    #
    #     if self.usr_delete is not None:
    #         if self.origem_delete_codigo == 'cliente':
    #             log['usr_delete'] = apps.get_model('cliente', 'ClienteLogin').objects.all().filter(id=self.usr_delete).first()
    #         elif self.origem_delete_codigo == 'funcionario':
    #             log['usr_delete'] = apps.get_model('funcionario', 'FuncionarioLogin').objects.all().filter(id=self.usr_delete).first()
    #         elif self.origem_delete_codigo == 'fornecedor':
    #             log['usr_delete'] = apps.get_model('fornecedor', 'FornecedorLogin').objects.all().filter(id=self.usr_delete).first()
    #         elif self.origem_delete_codigo == 'api':
    #             log['usr_delete'] = apps.get_model('api', 'ApiLogin').objects.all().filter(id=self.usr_delete).first()
    #
    #     return log


class ContatoLog(models.Model):
    celular_numero = models.CharField(max_length=50, null=True)
    celular_ddd = models.CharField(max_length=3, null=True)
    celular_completo = models.CharField(max_length=50, null=True)
    celular_completo_form = models.CharField(max_length=50, null=True)

    telefone_numero = models.CharField(max_length=50, null=True)
    telefone_ddd = models.CharField(max_length=3, null=True)
    telefone_completo = models.CharField(max_length=50, null=True)
    telefone_completo_form = models.CharField(max_length=50, null=True)

    email = models.EmailField(max_length=200, null=True)

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
    father = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    module = models.ForeignKey('core.Module', on_delete=models.DO_NOTHING, null=True)
    order = models.DecimalField(max_digits=10, decimal_places=4, null=True)

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


# Choices available throughout the project
class GenderTypes(models.TextChoices):
    MALE = ('male', _('Masculino'))
    FEMALE = ('female', _('Feminino'))
    OTHER = ('other', _('Outro'))
    NO_RESPONSE = ('no_response', _('Prefiro não responder'))


class CyrruncyTypes(models.TextChoices):
    REAL = ('BRL', _('R$ - Real'))
    EURO = ('EUR', _('€ - Euro'))
    DOLAR = ('USD', _('$ - Dólar'))
    CK_CROW = ('CZK', _('Kč - Coroa Tcheca'))
