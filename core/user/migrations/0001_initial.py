# Generated by Django 3.2.15 on 2023-04-02 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_first_login', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'public"."account',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('nm_full', models.CharField(max_length=200, null=True, verbose_name='Nome completo')),
                ('nm_first', models.CharField(max_length=200, null=True, verbose_name='Primeiro nome')),
                ('nm_last', models.CharField(max_length=200, null=True, verbose_name='Último nome')),
                ('person_id', models.BigIntegerField(unique=True, verbose_name='Identification of the person (id number, passport, etc)')),
                ('person_id_formatted', models.CharField(max_length=20, null=True, verbose_name='Formatted string of the person id')),
                ('id_type', models.CharField(choices=[('cpf', 'CPF'), ('passport', 'Passaporte')], default='cpf', max_length=100, null=True)),
                ('dat_birth', models.DateField(null=True)),
                ('nm_mother', models.CharField(max_length=200, null=True)),
                ('nm_father', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('sex', models.CharField(choices=[('male', 'Masculino'), ('female', 'Feminino'), ('other', 'Outro'), ('no_response', 'Prefiro não responder')], default='no_response', max_length=50)),
                ('hash', models.UUIDField(default=uuid.uuid4)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('image', models.FileField(null=True, upload_to='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_user_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_user_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_user_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'public"."user',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
