# Generated by Django 3.2 on 2022-08-08 00:50

import compositefk.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, null=True)),
                ('continent', models.CharField(max_length=5, null=True)),
                ('description', models.TextField(null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_country_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_country_deleted', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_country_last_edit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."country',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='UF',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, null=True)),
                ('nm_abrev', models.CharField(max_length=2, null=True)),
                ('cep_faixa_ini', models.CharField(max_length=80, null=True)),
                ('cep_faixa_fim', models.CharField(max_length=80, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_uf_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_uf_deleted', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_uf_last_edit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."uf',
                'abstract': False,
                'managed': True,
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('codigo', models.CharField(max_length=200, null=True)),
                ('informacao', models.CharField(max_length=500, null=True)),
                ('tipo', models.CharField(max_length=200, null=True)),
                ('nome', models.CharField(max_length=200, null=True)),
                ('descricao', models.TextField(null=True)),
                ('ordem', models.IntegerField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_tipo_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_tipo_deleted', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_tipo_last_edit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."tipo',
                'unique_together': {('codigo', 'tipo')},
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('order', models.IntegerField(null=True)),
                ('image', models.FileField(default='core/status/padrao.png', null=True, upload_to='core/status')),
                ('type', models.CharField(choices=[('library_item', 'Itens de Biblioteca'), ('library_reading', 'Status de leitura de item')], max_length=50, null=True)),
                ('grupo_codigo', models.CharField(max_length=200, null=True)),
                ('grupo_tipo', models.CharField(default='STATUS.GRUPO', max_length=200, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_status_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_status_deleted', to=settings.AUTH_USER_MODEL)),
                ('grupo', compositefk.fields.CompositeForeignKey(null=True, null_if_equal=[], on_delete=django.db.models.deletion.DO_NOTHING, related_name='status_grupo', to='core.tipo', to_fields={'codigo': compositefk.fields.LocalFieldValue('grupo_codigo'), 'tipo': compositefk.fields.LocalFieldValue('grupo_tipo')})),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_status_last_edit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."status',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, null=True)),
                ('local_code', models.CharField(max_length=50)),
                ('continent', models.CharField(max_length=5, null=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.country')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_region_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_region_deleted', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_region_last_edit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."country_region',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('cep_faixa_ini', models.CharField(max_length=80, null=True)),
                ('cep_faixa_fim', models.CharField(max_length=80, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_municipio_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_municipio_deleted', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_municipio_last_edit', to=settings.AUTH_USER_MODEL)),
                ('uf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.uf')),
            ],
            options={
                'db_table': 'public"."municipio',
                'abstract': False,
                'managed': True,
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_module_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_module_deleted', to=settings.AUTH_USER_MODEL)),
                ('father', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.module')),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_module_last_edit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."module',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('code', models.CharField(help_text='Exemplo: pt-br', max_length=10, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_language_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_language_deleted', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_language_last_edit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."language',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Cep',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('cep_form', models.CharField(max_length=15, null=True)),
                ('bairro_cep', models.CharField(max_length=100, null=True)),
                ('endereco_cep', models.CharField(max_length=100, null=True)),
                ('endereco_comp_cep', models.CharField(max_length=200, null=True)),
                ('latitude_cep', models.CharField(max_length=200, null=True)),
                ('longitude_cep', models.CharField(max_length=200, null=True)),
                ('tipo_cep', models.CharField(max_length=200, null=True)),
                ('cep', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_cep_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_cep_deleted', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_cep_last_edit', to=settings.AUTH_USER_MODEL)),
                ('municipio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.municipio')),
            ],
            options={
                'db_table': 'public"."cep',
                'abstract': False,
                'managed': True,
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dat_last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=500)),
                ('comments', models.TextField(null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_category_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_category_deleted', to=settings.AUTH_USER_MODEL)),
                ('father', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.category')),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='core_category_last_edit', to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.module')),
            ],
            options={
                'db_table': 'public"."category',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
