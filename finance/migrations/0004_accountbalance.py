# Generated by Django 4.2.3 on 2023-09-13 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0003_delete_accountbalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBalance',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('reference', models.IntegerField(help_text='Período de referência')),
                ('previous_balance', models.DecimalField(decimal_places=2, help_text='Saldo da conta no período anterior', max_digits=14)),
                ('incoming', models.DecimalField(decimal_places=2, help_text='Todas as entradas no período', max_digits=14)),
                ('outgoing', models.DecimalField(decimal_places=2, help_text='Todas as saídas no período', max_digits=14)),
                ('transactions', models.DecimalField(decimal_places=2, help_text='Saldo de entradas e saídas', max_digits=14)),
                ('earnings', models.DecimalField(decimal_places=2, help_text='Soma de todos os rendimentos da conta no período', max_digits=14)),
                ('transactions_balance', models.DecimalField(decimal_places=2, help_text='Soma das entradas e saídas mais os rendimentos', max_digits=14)),
                ('balance', models.DecimalField(decimal_places=2, help_text='Saldo da conta no período', max_digits=14)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.account')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."account_balance',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
