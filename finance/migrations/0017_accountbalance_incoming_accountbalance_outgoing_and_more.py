# Generated by Django 4.2.3 on 2023-08-27 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0016_accountbalance'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountbalance',
            name='incoming',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Todas as entradas no período', max_digits=14),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='outgoing',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Todas as saídas no período', max_digits=14),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='financedata',
            name='reference',
            field=models.IntegerField(default=202001),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountbalance',
            name='transactions',
            field=models.DecimalField(decimal_places=2, help_text='Saldo de entradas e saídas', max_digits=14),
        ),
        migrations.CreateModel(
            name='InvestmentStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('reference', models.SmallIntegerField()),
                ('gross_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('earnings', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.currency')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.investment')),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."investment_statement',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
