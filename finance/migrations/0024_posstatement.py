# Generated by Django 4.2.7 on 2024-01-10 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0023_investment_liquidated_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('edited_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('transaction_status', models.CharField(max_length=300, null=True)),
                ('method', models.CharField(max_length=200)),
                ('amount_gross', models.DecimalField(decimal_places=2, max_digits=14)),
                ('amount_discount', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('amount_fee', models.DecimalField(decimal_places=2, max_digits=14)),
                ('amount_net', models.DecimalField(decimal_places=2, max_digits=14)),
                ('transaction_date', models.DateTimeField()),
                ('settlement_date', models.DateTimeField()),
                ('credit_card_brand', models.CharField(max_length=150, null=True)),
                ('fee_detail', models.JSONField(help_text='Json tha contain all fees separately, the key is the name and value the amount', null=True)),
                ('cashFlow', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.cashflow')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."pos_statement',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]