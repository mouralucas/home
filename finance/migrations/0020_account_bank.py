# Generated by Django 3.2.15 on 2023-03-19 02:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0019_bankaccountmonthlybalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('code', models.SmallIntegerField(null=True)),
                ('name', models.CharField(max_length=150)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_bank_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_bank_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_bank_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."bank',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True, verbose_name='Descrição da conta')),
                ('branch', models.IntegerField(null=True)),
                ('branch_formatted', models.CharField(max_length=30, null=True)),
                ('account_number', models.IntegerField(null=True)),
                ('digit', models.SmallIntegerField(null=True)),
                ('account_number_formatted', models.CharField(max_length=150, null=True)),
                ('dat_open', models.DateField(help_text='Data de início do contrato', null=True)),
                ('dat_close', models.DateField(help_text='Data de fim do contrato', null=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.bank')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_account_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_account_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_account_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."account',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
